import logging
from datetime import datetime, timedelta
import pandas as pd

from src.viz.humidity_vizualizer import HumidityVizualizer
from src.viz.pressure_vizualizer import PressureVizualizer
from src.viz.temperature_vizualizer import TemperatureVizualizer

logger = logging.getLogger(__name__)


class DataVizualiserFactory:
    """
    Factory class responsible for generating data visualizations.

    It selects the appropriate visualizer based on the measurement type
    and pre-processes the data (filtering for the last 7 days) before plotting.
    """
    def plot(self, mesure_type: str, reports: pd.DataFrame):
        """
        Generates a plot for a specific measurement type.

        Args:
            mesure_type (str): Type of measurement to plot ("temperature", "humidity", "pressure").
            reports (pd.DataFrame): DataFrame containing the weather data.

        Returns:
            Any: The resulting plot object from the specific visualizer.

        Raises:
            ValueError: If the provided mesure_type is not supported.
        """
        # Filter data for the last 7 days
        if not reports.empty and 'date' in reports.columns:
            if not pd.api.types.is_datetime64_any_dtype(reports['date']):
                reports = reports.copy()
                reports['date'] = pd.to_datetime(reports['date'])

            # Time zone management to avoid comparison errors
            if reports['date'].dt.tz is not None:
                cutoff_date = pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=7)
            else:
                cutoff_date = datetime.now() - timedelta(days=7)

            reports = reports[reports['date'] >= cutoff_date]

        if mesure_type == "temperature":
            return TemperatureVizualizer().plot(reports)
        elif mesure_type == "humidity":
            return HumidityVizualizer().plot(reports)
        elif mesure_type == "pressure":
            return PressureVizualizer().plot(reports)
        else:
            raise ValueError(f"Invalid mesure_type: {mesure_type}")
