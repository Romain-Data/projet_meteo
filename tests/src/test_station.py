import pytest
import pandas as pd

from projet.src.entities.station import Station
from projet.src.entities.weather_report import WeatherReport


def test_station_initialization(mocker):
    report = mocker.Mock(spec=WeatherReport)
    station = Station(123, "name", 1.23, 456, [report])

    assert station.id == 123
    assert station.name == "name"
    assert station.longitude == 1.23
    assert station.latitude == 456
    assert station.reports == [report]

def test_no_reports_return_empty_list():
    station = Station(123, "name", 1.23, 456)
    assert station.reports == []

def test_get_all_reports(mocker):
    # On crée des faux rapports
    report1 = mocker.Mock(spec=WeatherReport)
    report1.date = pd.to_datetime("2023-01-01")
    report1.temperature = 10
    report1.humidity = 50
    report1.pressure = 1013
    report1.display_date = "01 Jan"

    report2 = mocker.Mock(spec=WeatherReport)
    report2.date = pd.to_datetime("2023-01-02")
    report2.temperature = 12
    report2.humidity = 55
    report2.pressure = 1015
    report2.display_date = "02 Jan"

    station = Station(1, "Test", 0, 0, [report1, report2])
    
    df = station.get_all_reports()
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['date', 'temperature', 'humidity', 'pressure', 'display_date']
    assert df.iloc[0]['temperature'] == 10
    assert df.iloc[1]['temperature'] == 12

def test_get_latest_reports(mocker):
    report1 = mocker.Mock(spec=WeatherReport)
    report1.date = pd.to_datetime("2023-01-01")
    
    report2 = mocker.Mock(spec=WeatherReport)
    report2.date = pd.to_datetime("2023-01-05")  # Plus récent
    
    station = Station(1, "Test", 0, 0, [report1, report2])
    
    latest = station.get_latest_reports()
    assert latest == report2
