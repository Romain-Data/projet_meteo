from abc import ABC, abstractmethod
import logging
import pandas as pd
import requests

from projet.src.entities.station import Station

logger = logging.getLogger(__name__)


class IDataExtractor(ABC):

    @abstractmethod
    def extract():
        pass


class APIExtractor(IDataExtractor):

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
        logger.info(f"APIExtractor initialized with base_url: {base_url}")

    def extract(
            self,
            station: Station,
            url_base: str = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/",
            select: str = 'heure_de_paris, temperature_en_degre_c, humidite, pression'
    ) -> pd.DataFrame:
        """
        Fetches weather data records for a given station via API.

        Args:
            station (Station): Station object containing the target station's ID.
            url_base (str, optional): Base URL of the API endpoint. Defaults to Toulouse Métropole API.
            select (str, optional): Comma-separated list of fields to retrieve. Defaults to:
                - heure_de_paris (timestamp)
                - temperature_en_degre_c (temperature in °C)
                - humidite (humidity in %)
                - pression (pressure in Pa)

        Returns:
            pd.DataFrame: DataFrame containing the retrieved records with columns as specified in `select`.
                Rows are ordered by descending timestamp (most recent first).
                Returns empty DataFrame if no records match the criteria.

        API Query Details:
            - Time range: Last 4 days (heure_de_paris >= now(days=-4))
            - Temporal resolution: Hourly data (minute(heure_de_paris) = 0)
            - Data quality filters:
                - Temperature: -10°C to 50°C
                - Humidity: 50% to 99%
            - Limit: 100 most recent records matching criteria
            """
        station_name = station.name
        station_id = station.id
        url_final = f"{url_base + station_id}/records"
        param = {
            'select': select,
            'where': """heure_de_paris >= now(days=-4)
                and minute(heure_de_paris) = 0
                and temperature_en_degre_c <= 50
                and temperature_en_degre_c >= -10
                and humidite >= 50
                and humidite < 100""",
            'order_by': 'heure_de_paris desc',
            'limit': '100'
        }

        try:
            logger.info(f"Fetching data for station '{station_name}' (ID: {station_id}) from {url_final}")
            logger.debug(f"Query parameters: {param}")

            response = requests.get(url_final, params=param, timeout=self.timeout)

            # Check HTTP status
            response.raise_for_status()

            # Parse JSON response
            json_data = response.json()

            # Extract results
            if 'results' not in json_data:
                logger.warning(f"No 'results' key in API response for station '{station_name}'")
                return pd.DataFrame()

            results = json_data['results']

            if not results:
                logger.warning(f"No data returned for station '{station_name}' (empty results)")
                return pd.DataFrame()

            df = pd.DataFrame(results)
            logger.info(f"Successfully fetched {len(df)} records for station '{station_name}'")
            logger.debug(f"DataFrame columns: {df.columns.tolist()}")

            return df

        except requests.exceptions.RequestException as errex:
            logger.error(f"Exception request: {errex}")
            return pd.DataFrame()
