from src.entities.station import Station

class City:
    def __init__(self, name: str, stations: list[Station]) -> None:
        self.name: str = name
        self.stations: list[Station] = stations
