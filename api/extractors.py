import pandas as pd
import requests
from entities.station import Station


class IDataExtractor:
    def extract(self):
        pass

class APIExtractor(IDataExtractor):

    def extract(
                self,
                station: Station,
                url_base: str = "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/",
                select: str = 'heure_de_paris, temperature_en_degre_c, humidite, pression'
            )-> pd.DataFrame:
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
            'limit':'100'
        }
        
        data = requests.get(url_final, params=param)
        return pd.DataFrame(data.json()['results'])
