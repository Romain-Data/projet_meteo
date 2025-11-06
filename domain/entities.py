from datetime import datetime
import pandas as pd


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
    

    def get_latest_report(self) -> WeatherReport|None:
        """
        Returns the most recent WeatherReport from the station's reports.

        Returns:
            WeatherReport: The report with the latest datetime.
            None: If no reports are available.
        """
        return max(self.reports, key=lambda report: report.date, default=None)



class City:
    def __init__(self, name: str, stations: list[Station]) -> None:
        self.name: str = name
        self.stations: list[Station] = stations

    

