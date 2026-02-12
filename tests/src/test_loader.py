import pytest
import pandas as pd

from projet.src.services.loader import DataLoader, DataLoaderError
from projet.src.entities.station import Station
from projet.src.entities.weather_report import WeatherReport


@pytest.fixture
def station():
    return Station(
        station_id="1",
        name="Toulouse",
        longitude=1.44,
        latitude=43.6
    )


@pytest.fixture
def loader():
    return DataLoader()


@pytest.fixture
def valid_data():
    return pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01 12:00']),
        'temperature': [15.5],
        'humidity': [60],
        'pressure': [1013],
        'display_date': ['01 Janvier']
    })


def test_load_reports_valid_data(loader, station, valid_data, mocker):
    spy_validate = mocker.spy(loader, '_validate_columns')
    
    loader.load_reports(station, valid_data)
    
    assert len(station.reports) == 1
    assert isinstance(station.reports[0], WeatherReport)
    assert station.reports[0].temperature == 15.5
    spy_validate.assert_called_once_with(valid_data, station.name)

def test_load_reports_empty_df(loader, station):
    empty_df = pd.DataFrame()
    with pytest.raises(DataLoaderError):
        loader.load_reports(station, empty_df)

def test_load_reports_incomplete_df(loader, station, valid_data):
    incomplete_df = valid_data.drop(columns=['humidity'])
    with pytest.raises(DataLoaderError):
        loader.load_reports(station, incomplete_df)

def test_load_reports_generic_error(loader, station, valid_data, mocker):
    mocker.patch.object(loader, '_validate_columns', side_effect=Exception("Erreur inattendue"))

    with pytest.raises(DataLoaderError) as exc_info:
        loader.load_reports(station, valid_data)

    assert "Erreur inattendue" in str(exc_info.value)
