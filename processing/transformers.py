import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class DataTransformer:
    
    DATE_COLUMN = 'heure_de_paris'
    DISPLAY_DATE_COLUMN = 'display_date'
    
    def __init__(self, date_format: str = "%d/%m/%Y %Hh"):
        """
        Initialize the DataTransformer.
        
        Args:
            date_format: Format string for display date (default: "%d/%m/%Y %Hh")
        """
        self.date_format = date_format
        logger.info(f"DataTransformer initialized with date_format: {date_format}")
    
    
    def format_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform raw weather data by adding formatted display dates.
        
        Args:
            data: Raw DataFrame with datetime column
        
        Returns:
            pd.DataFrame: Transformed DataFrame with additional 'display_date' column.
                         Returns empty DataFrame if transformation fails.
        """
        try:
            if data.empty:
                logger.warning("Received empty DataFrame, returning empty DataFrame")
                return pd.DataFrame()
            
            if self.DATE_COLUMN not in data.columns:
                logger.error(f"Missing required column '{self.DATE_COLUMN}'")
                return pd.DataFrame()
            
            logger.info(f"Transforming DataFrame with {len(data)} records")
            
            data['heure_de_paris'] = pd.to_datetime(data['heure_de_paris'])
            data['display_date'] = data['heure_de_paris'].dt.strftime('%Y-%m-%d %H:%M')
            data['temperature_en_degre_c'] = data['temperature_en_degre_c'].astype(np.float64)
            data['humidite'] = data['humidite'].astype(np.int64)
            data['pression'] = data['pression'].astype(np.int64)
                
            logger.info(f"Successfully transformed {len(data)} records")
            return data
                
        except Exception as e:
            logger.error(f"Transformation failed: {type(e).__name__} - {str(e)}")
            return pd.DataFrame()