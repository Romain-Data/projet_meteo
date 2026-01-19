"""
Module for extracting weather data from the Toulouse Métropole API.
"""

from abc import ABC, abstractmethod
import logging
import pandas as pd
import requests

from projet.src.entities.station import Station

logger = logging.getLogger(__name__)


class IDataExtractor(ABC):
    """
    Interface for data extraction.
    """
    # pylint: disable=too-few-public-methods

    @abstractmethod
    def extract(self, station: Station, **kwargs) -> pd.DataFrame:
        """
        Extract data from the API.

        Args:
            station (Station): Station object containing the target station's ID.
            **kwargs: Additional arguments for extraction configuration.

        Returns:
            pd.DataFrame: DataFrame containing the retrieved records.
        """


class APIExtractor(IDataExtractor):
    """
    Extracts weather data from the Toulouse Métropole API.
    """
    # pylint: disable=too-few-public-methods

    def __init__(
            self,
            base_url: str = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/",
            timeout: int = 30
    ):
        """
        Initialize the API extractor.

        Args:
            base_url: Base URL of the API
            timeout: Request timeout in seconds (default: 10)
        """
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        logger.info("APIExtractor initialized with base_url: %s", base_url)

    def extract(
            self,
            station: Station,
            url_base: str = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/",
            select: str = 'heure_de_paris, temperature_en_degre_c, humidite, pression',
            **kwargs
    ) -> pd.DataFrame:
        """
        Fetches weather data records for a given station via API.

        Args:
            station (Station): Station object containing the target station's ID.
            url_base (str, optional):
                Base URL of the API endpoint. Defaults to Toulouse Métropole API.
            select (str, optional): Comma-separated list of fields to retrieve. Defaults to:
                - heure_de_paris (timestamp)
                - temperature_en_degre_c (temperature in °C)
                - humidite (humidity in %)
                - pression (pressure in Pa)

        Returns:
            pd.DataFrame:
                DataFrame containing the retrieved records with columns as specified in `select`.
                Rows are ordered by descending timestamp (most recent first).
                Returns empty DataFrame if no records match the criteria.

        API Query Details:
            - Time range: Last 7 days (heure_de_paris >= now(days=-7))
            - Temporal resolution: Hourly data (minute(heure_de_paris) = 0)
            - Limit: 100 most recent records matching criteria
            """
        station_name = station.name
        station_id = station.id
        url_final = f"{url_base + station_id}/records"
        param = {
            'select': select,
            'where': 'heure_de_paris >= now(days=-7) and minute(heure_de_paris) = 0',
            'order_by': 'heure_de_paris desc',
            'limit': '100'
        }

        try:
            logger.info(
                "Fetching data for station %s (ID: %s) from %s",
                station_name,
                station_id,
                url_final
            )
            logger.debug("Query parameters: %s", param)

            response = requests.get(url_final, params=param, timeout=self.timeout)

            response.raise_for_status()

            json_data = response.json()

            if 'results' not in json_data:
                logger.warning("No 'results' key in API response for station %s", station_name)
                return pd.DataFrame()

            results = json_data['results']

            if not results:
                logger.warning("No data returned for station %s (empty results)", station_name)
                return pd.DataFrame()

            df = pd.DataFrame(results)
            logger.info("Successfully fetched %d records for station %s", len(df), station_name)
            logger.debug("DataFrame columns: %s", df.columns.tolist())

            return df

        except requests.exceptions.RequestException as errex:
            logger.error("Exception request: %s", errex)
            return pd.DataFrame()
