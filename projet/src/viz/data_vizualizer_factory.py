import logging
from datetime import datetime, timedelta
import pandas as pd

from src.viz.humidity_vizualizer import HumidityVizualizer
from src.viz.pressure_vizualizer import PressureVizualizer
from src.viz.temperature_vizualizer import TemperatureVizualizer

logger = logging.getLogger(__name__)


class DataVizualiserFactory:
    def plot(self, mesure_type: str, reports: pd.DataFrame):
        # Filtrer les données pour les 7 derniers jours
        if not reports.empty and 'date' in reports.columns:
            if not pd.api.types.is_datetime64_any_dtype(reports['date']):
                reports = reports.copy()
                reports['date'] = pd.to_datetime(reports['date'])

            # Gestion des timezones pour éviter l'erreur de comparaison
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
