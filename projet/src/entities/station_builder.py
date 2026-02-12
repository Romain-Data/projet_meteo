"""
Module for building Station objects.
"""

from .station import Station


class StationBuilder:
    """
    Builder for creating Station objects.
    """
    def __init__(self):
        """
        Initialize a new StationBuilder.
        """
        self.nom = ""
        self.id = ""
        self.longitude = ""
        self.latitude = ""
        self.reports = []

    def set_nom(self, nom: str) -> "StationBuilder":
        """
        Set the name of the station.

        Args:
            nom: Name of the station

        Raises:
            TypeError: If nom is not a string.
            ValueError: If nom is empty.
        """
        if not isinstance(nom, str):
            raise TypeError(f"nom must be a string, got {type(nom).__name__}")
        if not nom:
            raise ValueError("nom must not be empty")
        self.nom = nom
        return self

    def set_id(self, station_id: int | str) -> "StationBuilder":
        """
        Set the ID of the station.

        Args:
            station_id: ID of the station

        Raises:
            TypeError: If station_id is not a string or int.
            ValueError: If station_id is empty.
        """
        if not isinstance(station_id, (str, int)):
            raise TypeError(f"station_id must be a string or int, got {type(station_id).__name__}")
        if not station_id:
            raise ValueError("station_id must not be empty")
        self.id = station_id
        return self

    def set_longitude(self, longitude: float | int) -> "StationBuilder":
        """
        Set the longitude of the station.

        Args:
            longitude: Longitude of the station

        Raises:
            TypeError: If longitude is not a number.
        """
        if not isinstance(longitude, (float, int)):
            raise TypeError(f"longitude must be a number, got {type(longitude).__name__}")
        self.longitude = longitude
        return self

    def set_latitude(self, latitude: float | int) -> "StationBuilder":
        """
        Set the latitude of the station.

        Args:
            latitude: Latitude of the station

        Raises:
            TypeError: If latitude is not a number.
        """
        if not isinstance(latitude, (float, int)):
            raise TypeError(f"latitude must be a number, got {type(latitude).__name__}")
        self.latitude = latitude
        return self

    def set_reports(self, reports: list) -> "StationBuilder":
        """
        Set the reports of the station.

        Args:
            reports: Reports of the station

        Raises:
            TypeError: If reports is not a list.
        """
        if not isinstance(reports, list):
            raise TypeError(f"reports must be a list, got {type(reports).__name__}")
        self.reports = reports
        return self

    def build(self):
        """
        Build the station.

        Returns:
            Station: The built station
        """
        return Station(
            self.id,
            self.nom,
            self.longitude,
            self.latitude,
            self.reports
        )
