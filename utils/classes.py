from datetime import datetime
import numpy as np
import pandas as pd
import requests

class WeatherReport:
    def __init__(self, date: datetime, temperature: float, humidity: int, pressure: int, display_date: str) -> None:
        self.date: datetime = date
        self.temperature : float = temperature
        self.humidity: int = humidity
        self.pressure: int = pressure
        self.display_date: str = display_date


class Station:
    def __init__(self, id: str, name: str, reports: list[WeatherReport] = []) -> None:
        self.id: str = id
        self.name: str = name
        self.reports: list[WeatherReport] = reports

    def get_all_reports(self)-> pd.DataFrame:
        """Get all weather reports into one dataframe

        Returns:
            pd.DataFrame: pd.DataFrame: DataFrame avec les colonnes:
                - date (datetime)
                - temperature (float)
                - humidity (int)
                - pressure (int)
                - display_date (str)
        """
        data = [{
            'date': report.date,
            'temperature': report.temperature,
            'humidity': report.humidity,
            'pressure': report.pressure,
            'display_date': report.display_date
        } for report in self.reports]

        return pd.DataFrame(data)


class City:
    def __init__(self, name: str, stations: list[Station]) -> None:
        self.name: str = name
        self.stations: list[Station] = stations


# class DateUtil():

#     @staticmethod
#     def today_date():
#         return datetime.now()
    
#     @staticmethod
#     def last_week_date():
#         today = datetime.now()
#         last_3_days_date = (today - timedelta(days= 3)).strftime("%Y-%m-%d")
#         return last_3_days_date
    

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
        """Fetches weather data records for a given station via API.

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


class DataTransformer:
    def format_datime(self, data: pd.DataFrame) -> pd.DataFrame:
        """Formats datetime column in the DataFrame for display and processing.

        Args:
            data (pd.DataFrame): Input DataFrame containing a 'heure_de_paris' column
                with datetime values (as string or datetime objects).

        Returns:
            pd.DataFrame: Modified DataFrame with two datetime-related columns:
                - 'heure_de_paris': Original column converted to pandas datetime type
                (for calculations/filtering).
                - 'display_hour': Formatted string version (YYYY-MM-DD HH:MM)
                for display purposes.
        """

        data['heure_de_paris'] = pd.to_datetime(data['heure_de_paris'])
        data['display_date'] = data['heure_de_paris'].dt.strftime('%Y-%m-%d %H:%M')  
        return data 


class DataTester:
    def is_format_correct(self, data: pd.DataFrame) -> bool:
        pressure_is_int = data['pression'].dtype == np.int64
        humidity_is_int = data['humidite'].dtype == np.int64
        temperature_is_float = data['temperature_en_degre_c'].dtype == np.float64
        heure_is_datetime = pd.api.types.is_datetime64_any_dtype(data['heure_de_paris'])
        return pressure_is_int and humidity_is_int and temperature_is_float and heure_is_datetime
        
    def are_values_valid(self, data: pd.DataFrame) -> bool:
        aberrant_temperature = bool(len(data['temperature_en_degre_c'].between(50, -10, inclusive='both')))
        aberrant_humidity = bool(len(data['humidite'].between(95, 40, inclusive='both')))
        aberrant_pressure = bool(len(data['pression'].between(102000, 99500, inclusive='both')))
        return aberrant_temperature and aberrant_humidity and aberrant_pressure


class DataLoader:
    def add_reports(self, station: Station, data: pd.DataFrame)-> None:
        list_reports = []
        for _, row in data.iterrows():
            report = WeatherReport(
                date = row['heure_de_paris'],
                temperature = row['temperature_en_degre_c'],
                humidity = row['humidite'],
                pressure = row['pression'],
                display_date = row['display_date']
            )
            list_reports.append(report)
        station.reports=list_reports