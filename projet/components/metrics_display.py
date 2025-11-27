import streamlit as st
import pandas as pd


class MetricsDisplay:
    """Handles display of current weather metrics."""

    @staticmethod
    def render_statistics(df_reports: pd.DataFrame):
        """
        Render expandable statistics section.

        Args:
            df_reports: DataFrame containing all weather reports
        """
        with st.expander("📈 Statistics"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Min Temperature",
                    f"{df_reports['temperature'].min()}°C"
                )

            with col2:
                st.metric(
                    "Max Temperature",
                    f"{df_reports['temperature'].max()}°C"
                )

            with col3:
                st.metric(
                    "Avg Temperature",
                    f"{df_reports['temperature'].mean():.1f}°C"
                )
