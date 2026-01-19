"""
Module for displaying station information.
"""

from projet.src.entities.station import Station


class StationDisplayDecorator:
    """
    Decorator for displaying station information.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, station: Station):
        """
        Initialize a new StationDisplayDecorator.

        Args:
            station: The station to display
        """
        self.station = station

    def show(self):
        """
        Display the station information.
        """
        print(f"Station: {self.station.name}")
        for report in self.station.reports:
            print(f"- {report.display_date}: {report.temperature}°C")
