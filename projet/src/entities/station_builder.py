from src.entities.station import Station


class StationBuilder:
    def __init__(self):
        self.nom = ""
        self.id = ""
        self.longitude = ""
        self.latitude = ""
        self.reports = []

    def set_nom(self, nom):
        self.nom = nom
        return self

    def set_id(self, id):
        self.id = id
        return self

    def set_longitude(self, longitude):
        self.longitude = longitude
        return self

    def set_latitude(self, latitude):
        self.latitude = latitude
        return self

    def set_reports(self, reports):
        self.reports = reports
        return self

    def build(self):
        return Station(
            self.nom,
            self.id,
            self.longitude,
            self.latitude,
            self.reports
        )
