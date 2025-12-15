import logging
import streamlit as st

from projet.app_init import AppInitializer
from projet.components.sidebar import Sidebar
from projet.components.metrics_display import MetricsDisplay
from projet.components.navigation_header import NavigationHeader
from projet.config.config_loader import ConfigLoader
from projet.config.logging_config import setup_logging
from projet.src.data_structures.linked_list_navigator import LinkedListNavigator

setup_logging(log_level="INFO", log_file="weather_app.log")
logger = logging.getLogger(__name__)


def main():
    try:
        # 1. APPLICATION SETUP
        config = ConfigLoader()
        AppInitializer.setup_logging()
        AppInitializer.configure_page()

        init = AppInitializer(config)
        parquet_handler, data_fetcher, weather_charts = init.init_services()
        logger.info("Lancement de l'appli")

        # 2. NAVIGATION INITIALIZATION
        if 'navigator' not in st.session_state:
            stations = init.load_stations()
            st.session_state.navigator = LinkedListNavigator(stations)

            # Initialiser l'ID de la station courante
            first_station = st.session_state.navigator.get_current()
            st.session_state.selected_station_id = first_station.id

            logger.info(f"Navigator initialized with {len(stations)} stations")

        # 3. PAGE TITLE
        st.title(config.get('app.page_title', "🌡️ Weather Station Dashboard"))
        st.markdown("---")

        # 4. NAVIGATION CONTROLS
        NavigationHeader.render(st.session_state.navigator)

        # 5. SIDEBAR (with station selector)
        sidebar = Sidebar(parquet_handler, data_fetcher)
        sidebar.render(st.session_state.navigator)

        # 6. GET CURRENT STATION (source of truth)
        current_station = st.session_state.navigator.get_current()

        logger.info(f"Displaying data for station: {current_station.name}")

        # 7. LOAD STATION DATA
        parquet_handler.load_station_reports(current_station)

        if not current_station.reports:
            st.warning(f"No data available for '{current_station.name}'")
            st.info("Click 'Refresh Data' to fetch initial data")
            return

        # 8. DISPLAY STATION INFO
        latest_report = current_station.get_latest_report()

        st.header(f"📍 {current_station.name}")
        st.caption(f"Last update: {latest_report.display_date}")
        st.markdown("---")

        # 9. DISPLAY CHARTS AND METRICS
        st.header("📊 Temperature Timeline")
        df_reports = current_station.get_all_reports()

        if not df_reports.empty:
            fig_temp = weather_charts.plot("temperature", df_reports)
            st.plotly_chart(fig_temp, width='stretch')

            # Display statistics
            metrics_display = MetricsDisplay()
            metrics_display.render_statistics(df_reports)
        else:
            st.info("Not enough data to display chart")

    except Exception as e:
        logger.critical(f"Erreur fatale: {e}", exc_info=True)
        st.error(f"An application error occurred: {e}")


if __name__ == "__main__":
    main()
