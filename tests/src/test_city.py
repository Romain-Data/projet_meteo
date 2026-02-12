import pytest

from projet.src.entities.city import City
from projet.src.entities.station import Station


def test_city_initialization():
    station1 = Station("1", "station_1", 1.123, 1.123)
    station2 = Station("2", "station_2", 1.123, 1.123)
    liste_stations = [station1, station2]
    ville = City("Toulouse", liste_stations)

    assert ville.name == "Toulouse"
    assert ville.stations == liste_stations
    assert len(ville.stations) == 2

def test_empty_city():
    "Cas limite : ville vide"
    ville_vide = City("Ville Fantôme", [])

    assert ville_vide.name == "Ville Fantôme"
    assert ville_vide.stations == []
