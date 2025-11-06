import numpy as np
import pandas as pd

class DataValidator:
    def is_format_correct(self, data: pd.DataFrame) -> bool:
        """
        Validate that DataFrame columns have the expected data types.
        
        Args:
            data: DataFrame containing weather data columns
        
        Returns:
            True if all columns have correct types (pressure: int64, humidity: int64,
            temperature: float64, time: datetime64), False otherwise
        """
        pressure_is_int = data['pression'].dtype == np.int64
        humidity_is_int = data['humidite'].dtype == np.int64
        temperature_is_float = data['temperature_en_degre_c'].dtype == np.float64
        heure_is_datetime = pd.api.types.is_datetime64_any_dtype(data['heure_de_paris'])

        return pressure_is_int and humidity_is_int and temperature_is_float and heure_is_datetime
        
    def are_values_valid(self, data: pd.DataFrame) -> bool:
        """
        Check if all weather measurements fall within valid ranges.
        
        Validates that temperature, humidity, and pressure values are within
        physically reasonable bounds for all records.
        
        Args:
            data: DataFrame containing weather measurements
        
        Returns:
            True if all values are valid (temperature: -10 to 50°C, 
            humidity: 0 to 100%, pressure: 95000 to 105000 Pa), False otherwise
        """
        valid_temperature = data['temperature_en_degre_c'].between(-10, 50, inclusive='both').all()
        valid_humidity = data['humidite'].between(0, 100, inclusive='both').all()
        valid_pressure = data['pression'].between(95000, 105000, inclusive='both').all()
        
        return bool(valid_temperature and valid_humidity and valid_pressure)
