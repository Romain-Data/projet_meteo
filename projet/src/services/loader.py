"""
Module for loading validated weather data into Station entities.
"""

import logging
import pandas as pd
from projet.src.entities.station import Station
from projet.src.entities.weather_report import WeatherReport

logger = logging.getLogger(__name__)


class DataLoaderError(Exception):
    """Exception raised for any DataLoader error."""


class DataLoader:
    """
    Loads validated weather data into Station entities.
    """
    # pylint: disable=too-few-public-methods

    REQUIRED_COLUMNS = {'date', 'temperature', 'humidity', 'pressure'}

    def load_reports(self, station: Station, data: pd.DataFrame) -> None:
        """
        Convert DataFrame rows to WeatherReport objects and add to station.

        Args:
            station: Target Station entity to populate
            data: Validated DataFrame with columns:
                - heure_de_paris (datetime)
                - temperature_en_degre_c (float)
                - humidite (int)
                - pression (int)
                - display_date (str)

        Side Effects:
            Replaces station.reports with new list of WeatherReport objects
        """
        try:
            if data.empty:
                raise DataLoaderError(
                    f"Cannot load reports from empty DataFrame for station {station.name}"
                )

            self._validate_columns(data, station.name)
            logger.debug(
                "Validated %d rows for station %s",
                len(data),
                station.name
            )

            reports = [
                self._create_report(row)
                for _, row in data.iterrows()
            ]

            station.reports = reports
            logger.info(
                "Loaded %d reports for station %s",
                len(reports),
                station.name
            )

        except DataLoaderError:
            raise
        except Exception as e:
            logger.error(
                "Failed to load reports for station %s: %s",
                station.name,
                e,
                exc_info=True
            )
            raise DataLoaderError(
                f"Failed to load reports for station {station.name}: {e}"
            ) from e

    def _validate_columns(self, data: pd.DataFrame, station_name: str) -> None:
        """
        Validate that all required columns exist.

        Args:
            data: DataFrame (expected to be already normalized)
            station_name: Name of station (for error messages)

        Raises:
            DataLoaderError: If required columns are missing
        """
        missing = self.REQUIRED_COLUMNS - set(data.columns)

        if missing:
            raise DataLoaderError(
                f"Missing required columns for station {station_name}: {missing}. "
                "Data must be transformed by DataTransformer before loading."
            )

    def _create_report(self, row: pd.Series) -> WeatherReport:
        """
        Create a single WeatherReport from a DataFrame row.

        Args:
            row: pandas Series with weather data

        Returns:
            WeatherReport: Initialized weather report object
        """
        return WeatherReport(
            date=row['date'],
            temperature=row['temperature'],
            humidity=row['humidity'],
            pressure=row['pressure'],
            display_date=row['display_date']
        )
