import logging
import pandas as pd
import inspect

from projet.src.viz.humidity_vizualizer import HumidityVizualizer
from projet.src.viz.pressure_vizualizer import PressureVizualizer
from projet.src.viz.temperature_vizualizer import TemperatureVizualizer

logger = logging.getLogger(__name__)


class DataVizualiserFactory:
    def plot(self, mesure_type: str, reports: pd.DataFrame):
        if mesure_type == "temperature":
            viz = TemperatureVizualizer()
            if not hasattr(viz, 'plot'):
                logger.error(f"DEBUG: Le fichier chargé est ICI : {inspect.getfile(TemperatureVizualizer)}")
                logger.error(f"DEBUG: L'objet {viz} ne contient pas 'plot'. Attributs disponibles : {dir(viz)}")
            return viz.plot(reports)
        elif mesure_type == "humidity":
            return HumidityVizualizer().plot(reports)
        elif mesure_type == "pressure":
            return PressureVizualizer().plot(reports)
        else:
            raise ValueError(f"Invalid mesure_type: {mesure_type}")
