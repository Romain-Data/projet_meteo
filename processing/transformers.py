import numpy as np
import pandas as pd

class DataTransformer:
    def format_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Convert DataFrame columns to appropriate types for Parquet storage.
        
        Transforms datetime strings and ensures numeric types are optimized
        for efficient storage and retrieval.
        
        Args:
            data (pd.DataFrame): Raw DataFrame with weather data containing:
                - heure_de_paris: datetime string
                - temperature_en_degre_c: temperature values
                - humidite: humidity percentage
                - pression: pressure in Pascals
        
        Returns:
            pd.DataFrame: DataFrame with properly typed columns:
                - heure_de_paris: datetime64[ns]
                - display_date: formatted string (YYYY-MM-DD HH:MM)
                - temperature_en_degre_c: float32
                - humidite: int16
                - pression: int32
        """
        data['heure_de_paris'] = pd.to_datetime(data['heure_de_paris'])
        data['display_date'] = data['heure_de_paris'].dt.strftime('%Y-%m-%d %H:%M')
        
        # ✅ Conversion explicite des types (important pour Parquet)
        data['temperature_en_degre_c'] = data['temperature_en_degre_c'].astype(np.float64)
        data['humidite'] = data['humidite'].astype(np.int64)
        data['pression'] = data['pression'].astype(np.int64)
        
        return data
