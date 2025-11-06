import numpy as np
import pandas as pd

class DataValidator:
    def is_format_correct(self, data: pd.DataFrame) -> bool:
        pressure_is_int = data['pression'].dtype == np.int64
        humidity_is_int = data['humidite'].dtype == np.int64
        temperature_is_float = data['temperature_en_degre_c'].dtype == np.float64
        heure_is_datetime = pd.api.types.is_datetime64_any_dtype(data['heure_de_paris'])
        return pressure_is_int and humidity_is_int and temperature_is_float and heure_is_datetime
        
    def are_values_valid(self, data: pd.DataFrame) -> bool:
        # Vérifier que TOUTES les valeurs sont dans les plages valides
        valid_temperature = data['temperature_en_degre_c'].between(-10, 50, inclusive='both').all()
        valid_humidity = data['humidite'].between(0, 100, inclusive='both').all()
        valid_pressure = data['pression'].between(95000, 105000, inclusive='both').all()
        
        return bool(valid_temperature and valid_humidity and valid_pressure)
