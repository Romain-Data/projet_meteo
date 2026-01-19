"""
Module for creating pressure visualizations.
"""

import logging
import pandas as pd
import plotly.graph_objects as go

from projet.src.viz import viz_utils

logger = logging.getLogger(__name__)


class PressureVizualizer:
    """
    Class for creating pressure visualizations.
    """
    # pylint: disable=too-few-public-methods

    def plot(self, reports: pd.DataFrame) -> go.Figure:
        """
        Create an interactive line plot of pressure over time.

        Args:
            reports: DataFrame with 'date' (datetime) and 'pressure' (int) columns

        Returns:
            go.Figure: Plotly figure object with pressure timeline
        """
        return viz_utils.create_time_series_chart(
            df=reports,
            y_col='pressure',
            title="Pressure Over Time",
            y_title="Pressure (Pa)",
            color='#2ca02c'
        )
