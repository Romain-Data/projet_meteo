"""
Module for transforming weather data.
"""

import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataTransformer:
    """
    Class for transforming weather data.
    """

    DATE_COLUMN = 'heure_de_paris'
    DISPLAY_DATE_COLUMN = 'display_date'

    def __init__(self, date_format: str = "%d/%m/%Y %Hh"):
        """
        Initialize the DataTransformer.

        Args:
            date_format: Format string for display date
                Default: "%d/%m/%Y %Hh"
        """
        self.date_format = date_format
        logger.info("DataTransformer initialized with date_format: %s", date_format)

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
                logger.error("Missing required column '%s'", self.DATE_COLUMN)
                return pd.DataFrame()

            logger.info("Transforming DataFrame with %s records", len(data))

            data['heure_de_paris'] = pd.to_datetime(data['heure_de_paris'])
            data['display_date'] = data['heure_de_paris'].dt.strftime('%Y-%m-%d %H:%M')
            data['temperature_en_degre_c'] = data['temperature_en_degre_c'].astype(np.float64)
            data['humidite'] = data['humidite'].astype(np.int64)
            data['pression'] = data['pression'].astype(np.int64)

            logger.info("Successfully transformed %s records", len(data))
            return data

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Transformation failed: %s - %s", type(e).__name__, str(e))
            return pd.DataFrame()

    def normalize_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names to internal format.

        Handles both API format (FR) and Parquet format (EN).
        """
        df = data.copy()

        # Mapping: API/Parquet
        column_mapping = {
            'heure_de_paris': 'date',
            'temperature_en_degre_c': 'temperature',
            'humidite': 'humidity',
            'pression': 'pressure'
        }

        # Rename only the columns that exist
        df = df.rename(columns={
            k: v for k, v in column_mapping.items()
            if k in df.columns
        })

        # Generates display_date if absent
        if 'display_date' not in df.columns:
            df['display_date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

        return df
