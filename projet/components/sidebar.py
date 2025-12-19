import streamlit as st
from projet.src.data_structures.linked_list_navigator import LinkedListNavigator
from projet.src.services.data_fetcher import DataFetcher
from projet.src.storage.parquet_handler import ParquetHandler
from projet.src.api.request_queue import ApiRequestQueue


class Sidebar:
    """Handles sidebar UI and interactions."""

    def __init__(self, parquet_handler: ParquetHandler, data_fetcher: DataFetcher, api_queue: ApiRequestQueue):
        """
        Initialize Sidebar with required services.

        Args:
            parquet_handler: Service for Parquet file operations
            data_fetcher: Service for API data fetching
        """
        self.parquet_handler = parquet_handler
        self.data_fetcher = data_fetcher
        self.api_queue = api_queue

    def render(self, navigator: 'LinkedListNavigator'):
        """
        Render sidebar with station selection and refresh button.
        Synchronizes with the navigator when user selects a different station.

        Args:
            navigator: The LinkedListNavigator instance
        """
        with st.sidebar:
            st.header("⚙️ Configuration")

            # Get all stations and current station from navigator
            all_stations = navigator.get_all_stations()
            current_station = navigator.get_current()

            # Build station lookup: {id: (name, station_object)}
            station_options = {
                station.id: station.name
                for station in all_stations
            }

            # Get current selection from session state (source of truth)
            current_id = st.session_state.get('selected_station_id', current_station.id)

            # Find the index of the current station in the list
            station_ids = list(station_options.keys())
            try:
                current_index = station_ids.index(current_id)
            except ValueError:
                # Fallback if ID not found
                current_index = 0
                st.session_state.selected_station_id = station_ids[0]

            # Station selector (jump to)
            selected_id = st.selectbox(
                "Choose a station",
                options=station_ids,
                format_func=lambda x: station_options[x],
                index=current_index,
                key=f"station_selector_{current_id}"
            )

            # Synchronize navigator if selection changed
            if selected_id != current_id:
                # Find the selected station object
                selected_station = next(
                    (station for station in all_stations if station.id == selected_id),
                    None
                )
                if selected_station:
                    navigator.set_current(selected_station)
                    st.session_state.selected_station_id = selected_station.id
                    self.api_queue.add_task(
                        self.data_fetcher.refresh_and_save_station_data,
                        station=selected_station
                    )
                    st.rerun()

            st.markdown("---")
            self._render_refresh_button(current_station)

            return current_station

    def _render_refresh_button(self, station):
        """
        Render and handle refresh data button.

        Args:
            station: Station object to refresh data for
        """
        if st.button("🔄 Refresh Data", width='stretch'):
            st.toast(f"Adding refresh task for {station.name} to the queue...")
            self.api_queue.add_task(
                self.data_fetcher.refresh_and_save_station_data,
                station=station,
            )
            st.info("Refresh is running in the background.")
            st.rerun()
