import pytest
from projet.src.entities.station_display_decorator import StationDisplayDecorator

@pytest.fixture
def mock_station(mocker):
    station = mocker.Mock(name="Station")
    station.name = "Paris"
    
    # Mock des reports
    r1 = mocker.Mock()
    r1.display_date = "2023-01-01 12:00"
    r1.temperature = 15.5
    
    r2 = mocker.Mock()
    r2.display_date = "2023-01-02 12:00"
    r2.temperature = 12.0
    
    station.reports = [r1, r2]
    return station

def test_display_decorator_show(mock_station, capsys):
    """Test : Affichage correct des informations de la station"""
    decorator = StationDisplayDecorator(mock_station)
    
    decorator.show()
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Station: Paris" in output
    assert "- 2023-01-01 12:00: 15.5°C" in output
    assert "- 2023-01-02 12:00: 12.0°C" in output

def test_display_decorator_empty_reports(mock_station, capsys):
    """Test : Affichage avec 0 reports"""
    mock_station.reports = []
    
    decorator = StationDisplayDecorator(mock_station)
    decorator.show()
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Station: Paris" in output
    assert "- " not in output
