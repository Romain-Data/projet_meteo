import logging
import streamlit as st

from app_init import AppInitializer
from config.config_loader import get_config
from components.sidebar import Sidebar
from components.metrics_display import MetricsDisplay

logger = logging.getLogger(__name__)


def main():
    # --- Application Setup ---
    # 1. Load configuration and setup logging first
    config = get_config()
    AppInitializer.setup_logging()
    
    # 2. Configure Streamlit page
    AppInitializer.configure_page()
    
    logger.info("Lancement de l'appli")
    
    # 3. Initialize services (cached) and data loader
    initializer = AppInitializer(config)
    parquet_handler, data_fetcher, weather_charts = AppInitializer.init_services()
    
    # --- Main Application Logic ---
    stations = initializer.load_stations()
    station_lookup = initializer.create_station_lookup(stations)
    st.title(config.get('app.page_title', "🌡️ Weather Station Dashboard"))
    st.markdown("---")
    
    # Render sidebar and get selected station
    sidebar = Sidebar(parquet_handler, data_fetcher)
    selected_station = sidebar.render(station_lookup)
    
    # Load station data
    parquet_handler.load_station_reports(selected_station)
    
    # Check if data exists
    if not selected_station.reports:
        st.warning(f"No data available for station '{selected_station.name}'")
        st.info("Click 'Refresh Data' to fetch initial data")
        return
    
    # Get latest report
    latest_report = selected_station.get_latest_report()
    
    # Display metrics
    metrics_display = MetricsDisplay()
    metrics_display.render_header(selected_station, latest_report.display_date)
    metrics_display.render_current_metrics(
        latest_report.temperature,
        latest_report.humidity,
        latest_report.pressure
    )
    
    st.markdown("---")
    
    # Display temperature chart
    st.header("📊 Temperature Timeline")
    df_reports = selected_station.get_all_reports()
    
    if not df_reports.empty:
        fig_temp = weather_charts.plot_temperature(df_reports)
        st.plotly_chart(fig_temp, use_container_width=True)
        metrics_display.render_statistics(df_reports)
    else:
        st.info("Not enough data to display chart")


if __name__ == "__main__":
    main()
