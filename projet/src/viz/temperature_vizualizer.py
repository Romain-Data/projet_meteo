"""
Module for creating temperature visualizations.
"""

import logging
import pandas as pd
import plotly.graph_objects as go

from projet.src.viz import viz_utils

logger = logging.getLogger(__name__)


class TemperatureVizualizer:
    """
    Class for creating temperature visualizations.
    """
    # pylint: disable=too-few-public-methods

    def plot(self, reports: pd.DataFrame) -> go.Figure:
        """
        Create an interactive line plot of temperature over time.

        Args:
            reports: DataFrame with 'date' (datetime) and 'temperature' (float) columns

        Returns:
            go.Figure: Plotly figure object with temperature timeline
        """
        return viz_utils.create_time_series_chart(
            df=reports,
            y_col='temperature',
            title="Temperature Over Time",
            y_title="Temperature (°C)",
            color='#FB8500'
        )
