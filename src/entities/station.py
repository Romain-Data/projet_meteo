import pandas as pd
from src.entities.weather_report import WeatherReport


class Station:
    def __init__(self, id: str, name: str, longitude: float, latitude: float,
                 reports: list[WeatherReport] = []) -> None:
        """Instantcie la classe Station

        Args:
            id (str): identitiant de la station
            name (str): nom de la station
            longitude (float)
            latitude (float)
            reports (list[WeatherReport], optional): 
                liste des rapports météo liés à la station. 
                Defaults to [].
        """
        self.id: str = id
        self.name: str = name
        self.longitude = longitude
        self.latitude = latitude
        self.reports: list[WeatherReport] = reports

    def get_all_reports(self) -> pd.DataFrame:
        """
        Get all weather reports into one dataframe

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
    
    def get_latest_report(self) -> WeatherReport:
        """
        Returns the most recent WeatherReport from the station's reports.

        Returns:
            WeatherReport: The report with the latest datetime.
            None: If no reports are available.
        """
        return max(self.reports, key=lambda report: report.date)
