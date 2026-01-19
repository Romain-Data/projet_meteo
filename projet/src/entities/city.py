"""
Module for representing a city with its weather stations.
"""

from .station import Station


class City:
    """
    Represents a city containing multiple weather stations.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, name: str, stations: list[Station]) -> None:
        """
        Initialize a new City.

        Args:
            name: Name of the city
            stations: List of weather stations in the city
        """
        self.name: str = name
        self.stations: list[Station] = stations
