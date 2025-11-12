import streamlit as st
import pandas as pd
from typing import Tuple

from src.entities.station import Station
from src.entities.weather_report import WeatherReport


class MetricsDisplay:
    """Handles display of current weather metrics."""
    
    @staticmethod
    def render_header(station: Station, latest_date: str):
        """
        Render station header with name and last update.
        
        Args:
            station: The weather station
            latest_date: Formatted date string of last update
        """
        st.header(f"📍 {station.name}")
        st.caption(f"Last update: {latest_date}")
    
    @staticmethod
    def render_current_metrics(weather_report: WeatherReport):
        """
        Render current weather metrics in three columns.
        
        Args:
            temperature: Current temperature in Celsius
            humidity: Current humidity percentage
            pressure: Current pressure in Pascals
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🌡️ Temperature",
                value=f"{weather_report.temperature}°C"
            )
        
        with col2:
            st.metric(
                label="💧 Humidity",
                value=f"{weather_report.humidity}%"
            )
        
        with col3:
            st.metric(
                label="🔽 Pressure",
                value=f"{weather_report.pressure} Pa"
            )
    
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
