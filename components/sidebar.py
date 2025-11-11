import streamlit as st
from typing import Dict

from src.entities.station import Station
from src.services.data_fetcher import DataFetcher
from src.storage.parquet_handler import ParquetHandler


class Sidebar:
    """Handles sidebar UI and interactions."""
    
    def __init__(
        self,
        parquet_handler: ParquetHandler,
        data_fetcher: DataFetcher
    ):
        self.parquet_handler = parquet_handler
        self.data_fetcher = data_fetcher
    
    def render(self, station_lookup: Dict[str, Station]) -> Station:
        """
        Render sidebar with station selection and refresh button.
        
        Args:
            station_lookup: Dictionary mapping station names to Station objects
            
        Returns:
            Station: The selected station
        """
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            selected_station = self._render_station_selector(station_lookup)
            
            st.markdown("---")
            
            self._render_refresh_button(selected_station)
            
            return selected_station
    
    def _render_station_selector(
        self,
        station_lookup: Dict[str, Station]
    ) -> Station:
        """Render station selection dropdown."""
        selected_name = st.selectbox(
            "Choose a station",
            options=list(station_lookup.keys()),
            index=0
        )
        return station_lookup[selected_name]
    
    def _render_refresh_button(self, station: Station):
        """Render and handle refresh data button."""
        if st.button("🔄 Refresh Data", use_container_width=True):
            with st.spinner("Fetching new data..."):
                self.data_fetcher.fetch_and_load(station)
                self.parquet_handler.save_station_reports(station)
                st.success("Data refreshed!")
                st.rerun()
