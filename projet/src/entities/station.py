"""
Module for representing a weather station.
"""

import pandas as pd
from .weather_report import WeatherReport


class Station:
    """
    Represents a weather station with its reports.
    """
    def __init__(self, station_id: str | int, name: str, longitude: float, latitude: float,
                 reports: list[WeatherReport] = None) -> None:
        """Instantiate the Station class

        Args:
            station_id (str | int): Station identifier
            name (str): Station name
            longitude (float)
            latitude (float)
            reports (list[WeatherReport], optional): List of weather reports linked to the station.
                Defaults to None.
        """
        # pylint: disable=too-many-arguments, too-many-positional-arguments
        # pylint: disable=too-many-instance-attributes
        if reports is None:
            reports = []
        self.id: str = station_id
        self.name: str = name
        self.longitude = longitude
        self.latitude = latitude
        self.reports: list[WeatherReport] = reports

    def get_all_reports(self) -> pd.DataFrame:
        """
        Get all weather reports into one dataframe

        Returns:
            pd.DataFrame: DataFrame with columns:
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

    def get_latest_reports(self) -> WeatherReport:
        """
        Returns the most recent WeatherReport from the station's reports.

        Returns:
            WeatherReport: The report with the latest datetime.
            None: If no reports are available.
        """
        return max(self.reports, key=lambda report: report.date)
