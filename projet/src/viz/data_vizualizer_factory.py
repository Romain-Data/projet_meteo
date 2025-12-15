import logging
import pandas as pd
from src.viz.humidity_vizualizer import HumidityVizualizer
from src.viz.pressure_vizualizer import PressureVizualizer
from src.viz.temperature_vizualizer import TemperatureVizualizer

logger = logging.getLogger(__name__)


class DataVizualiserFactory:
    def plot(mesure_type: str, reports: pd.DataFrame):
        if mesure_type == "temperature":
            return TemperatureVizualizer().plot(reports)
        elif mesure_type == "humidity":
            return HumidityVizualizer().plot(reports)
        elif mesure_type == "pressure":
            return PressureVizualizer().plot(reports)
        else:
            raise ValueError(f"Invalid mesure_type: {mesure_type}")
