"""
Module for creating humidity visualizations.
"""

import logging
import pandas as pd
import plotly.graph_objects as go

from projet.src.viz import viz_utils

logger = logging.getLogger(__name__)


class HumidityVizualizer:
    """
    Class for creating humidity visualizations.
    """
    # pylint: disable=too-few-public-methods

    def plot(self, reports: pd.DataFrame) -> go.Figure:
        """
        Create an interactive line plot of humidity over time.

        Args:
            reports: DataFrame with 'date' (datetime) and 'humidity' (int) columns

        Returns:
            go.Figure: Plotly figure object with humidity timeline
        """
        return viz_utils.create_time_series_chart(
            df=reports,
            y_col='humidity',
            title="Humidity Over Time",
            y_title="Humidity (%)",
            color='#1f77b4'
        )
