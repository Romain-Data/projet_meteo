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

    def set_nom(self, nom):
        """
        Set the name of the station.

        Args:
            nom: Name of the station
        """
        self.nom = nom
        return self

    def set_id(self, station_id):
        """
        Set the ID of the station.

        Args:
            station_id: ID of the station
        """
        self.id = station_id
        return self

    def set_longitude(self, longitude):
        """
        Set the longitude of the station.

        Args:
            longitude: Longitude of the station
        """
        self.longitude = longitude
        return self

    def set_latitude(self, latitude):
        """
        Set the latitude of the station.

        Args:
            latitude: Latitude of the station
        """
        self.latitude = latitude
        return self

    def set_reports(self, reports):
        """
        Set the reports of the station.

        Args:
            reports: Reports of the station
        """
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
