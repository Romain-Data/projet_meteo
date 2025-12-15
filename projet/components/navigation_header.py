import streamlit as st

from projet.src.api.request_queue import ApiRequestQueue
from projet.src.data_structures.linked_list_navigator import LinkedListNavigator
from projet.src.services.data_fetcher import DataFetcher


class NavigationHeader:
    """Handles station navigation display in the main area."""

    @staticmethod
    def render(navigator: LinkedListNavigator, api_queue: ApiRequestQueue, data_fetcher: DataFetcher):
        """
        Render navigation buttons above the station header.
        Synchronizes session state when navigation occurs.

        Args:
            navigator: The LinkedListNavigator instance
            api_queue: The background task queue.
            data_fetcher: The service for fetching data.
        """
        # Create 3 columns with empty middle column for spacing
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button("← Précédent", key="btn_previous", width='stretch'):
                previous_station = navigator.get_previous()
                if previous_station:
                    # Synchronize session state
                    st.session_state.selected_station_id = previous_station.id
                    api_queue.add_task(
                        data_fetcher.refresh_and_save_station_data,
                        station=previous_station
                    )
                    st.rerun()

        # col2 is intentionally left empty for spacing

        with col3:
            if st.button("Suivant →", key="btn_next", width='stretch'):
                next_station = navigator.get_next()
                if next_station:
                    # Synchronize session state
                    st.session_state.selected_station_id = next_station.id
                    api_queue.add_task(
                        data_fetcher.refresh_and_save_station_data,
                        station=next_station
                    )
                    st.rerun()
