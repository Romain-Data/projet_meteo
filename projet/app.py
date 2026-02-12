"""
Main entry point for the Weather Dashboard application.

This module sets up the Streamlit interface, initializes the application components
(navigator, sidebar, service), and handles the main event loop for user interactions.
"""

import logging
import time
import streamlit as st

from projet.app_init import AppInitializer
from projet.components.sidebar import Sidebar
from projet.components.metrics_display import MetricsDisplay
from projet.components.navigation_header import NavigationHeader
from projet.config.config_loader import ConfigLoader
from projet.config.logging_config import setup_logging
from projet.src.data_structures.linked_list_navigator import LinkedListNavigator
from projet.src.api.request_queue import ApiRequestQueue

setup_logging(log_level="INFO", log_file="weather_app.log")
logger = logging.getLogger(__name__)


def main():
    """ Main function to run the weather application. """
    try:
        # 1. APPLICATION SETUP
        config = ConfigLoader()
        AppInitializer.setup_logging()
        AppInitializer.configure_page()

        init = AppInitializer(config)
        parquet_handler, data_fetcher, weather_charts = init.init_services()
        logger.info("Lancement de l'appli")

        # Initialiser et démarrer la file d'attente une seule fois par session
        if 'api_queue' not in st.session_state:
            logger.info("Creating and starting a new ApiRequestQueue instance.")
            st.session_state.task_status = {"refresh_needed": False}
            st.session_state.api_queue = ApiRequestQueue(task_status=st.session_state.task_status)
            st.session_state.api_queue.start()

        # Vérifie si un rafraîchissement est nécessaire après une tâche de fond
        if st.session_state.task_status.get("refresh_needed", False):
            st.session_state.task_status["refresh_needed"] = False
            st.rerun()

        # Affiche un spinner et recharge tant que la file d'attente travaille
        if st.session_state.api_queue.is_working:
            with st.spinner("Mise à jour des données en cours..."):
                time.sleep(0.5)
                st.rerun()

        # 2. NAVIGATION INITIALIZATION
        if 'navigator' not in st.session_state:
            stations = init.load_stations()
            st.session_state.navigator = LinkedListNavigator(stations)

            # Initialiser l'ID de la station courante
            first_station = st.session_state.navigator.get_current()
            st.session_state.selected_station_id = first_station.id

            logger.info("Navigator initialized with %d stations", len(stations))

        # 3. PAGE TITLE
        st.title(config.get('app.page_title', "🌡️ Weather Station Dashboard"))
        st.markdown("---")

        # 4. NAVIGATION CONTROLS
        NavigationHeader.render(
            navigator=st.session_state.navigator,
            api_queue=st.session_state.api_queue,
            data_fetcher=data_fetcher
        )

        # 5. SIDEBAR (with station selector)
        sidebar = Sidebar(
            parquet_handler=parquet_handler,
            data_fetcher=data_fetcher,
            api_queue=st.session_state.api_queue)
        sidebar.render(st.session_state.navigator)

        # 6. GET CURRENT STATION (source of truth)
        current_station = st.session_state.navigator.get_current()

        logger.info("Displaying data for station: %s", current_station.name)

        # 7. LOAD STATION DATA
        parquet_handler.load_station_reports(current_station)

        if not current_station.reports:
            st.warning(f"No data available for '{current_station.name}'")
            st.info("Click 'Refresh Data' to fetch initial data")
            return

        _render_dashboard(current_station, weather_charts)

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.critical("Erreur fatale: %s", e, exc_info=True)
        st.error(f"An application error occurred: {e}")


def _render_dashboard(current_station, weather_charts):
    """
    Helper function to render the station dashboard (info, charts, metrics).
    Extracted from main() to reduce local variable count.
    """
    # 8. DISPLAY STATION INFO
    latest_reports = current_station.get_latest_reports()

    st.header(f"📍 {current_station.name}")
    st.caption(f"Last update: {latest_reports.display_date}")
    st.markdown("---")

    # 9. DISPLAY CHARTS AND METRICS
    st.header("📊 Weather Timeline")

    metric_options = {
        "Temperature": "temperature",
        "Humidity": "humidity",
        "Pressure": "pressure",
        "Surprise 🎁": "surprise"
    }
    selected_metric_label = st.selectbox("Select metric:", list(metric_options.keys()))
    selected_metric = metric_options[selected_metric_label]

    if selected_metric == "surprise":
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", autoplay=True)
    else:
        df_reports = current_station.get_all_reports()

        if not df_reports.empty:
            fig = weather_charts.plot(selected_metric, df_reports)
            st.plotly_chart(fig, width='stretch')

            # Display statistics
            metrics_display = MetricsDisplay()
            metrics_display.render_statistics(df_reports)
        else:
            st.info("Not enough data to display chart")


if __name__ == "__main__":
    main()
