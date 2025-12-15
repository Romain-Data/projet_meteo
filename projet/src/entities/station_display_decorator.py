from projet.src.entities.station import Station


class StationDisplayDecorator:
    def __init__(self, station: Station):
        self.station = station

    def show(self):
        print(f"Station: {self.station.name}")
        for report in self.station.reports:
            print(f"- {report.display_date}: {report.temperature}°C")
