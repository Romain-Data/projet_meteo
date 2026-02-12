import logging
import pytest
import pandas as pd
from pathlib import Path
from projet.app_init import AppInitializer

@pytest.fixture
def mock_config(mocker):
    config = mocker.Mock()
    config.get.return_value = "fake/path/stations.csv"
    config.get_section.return_value = {}
    config.get_required.side_effect = lambda k: {
        'api.url_base': 'http://test.com',
        'api.timeout': 10,
        'storage.data_path': './data',
        'storage.parquet_compression': 'snappy'
    }.get(k)
    return config

@pytest.fixture
def app_init(mock_config):
    return AppInitializer(mock_config)

# --- Tests load_stations ---

def test_load_stations_success(mocker, app_init):
    app_init.load_stations.clear()
    mocker.patch("projet.app_init.Path.exists", return_value=True)

    df_data = {
        'id_nom': ['S1', 'S2'],
        'nom': ['Station 1', 'Station 2'],
        'longitude': [1.1, 2.2],
        'latitude': [45.0, 46.0]
    }
    mocker.patch("pandas.read_csv", return_value=pd.DataFrame(df_data))

    stations = app_init.load_stations()

    assert len(stations) == 2
    assert stations[0].name == "Station 1"
    assert stations[1].id == "S2"

def test_load_stations_file_not_found(mocker, app_init, caplog):
    caplog.set_level(logging.ERROR)
    app_init.load_stations.clear()
    
    mock_path = mocker.patch("projet.app_init.Path")
    mock_path.return_value.exists.return_value = False

    with pytest.raises(FileNotFoundError):
        app_init.load_stations()
    assert "Stations file not found" in caplog.text

# --- Tests create_station_lookup ---

def test_create_station_lookup(mocker, app_init):
    s1 = mocker.Mock()
    s1.name = "Paris"
    s2 = mocker.Mock()
    s2.name = "Lyon"

    lookup = app_init.create_station_lookup([s1, s2])

    assert lookup["Paris"] == s1
    assert lookup["Lyon"] == s2
    assert len(lookup) == 2

# --- Tests configure_page & setup_logging ---

def test_configure_page(mocker):
    mock_st = mocker.patch("projet.app_init.st")
    mock_conf_cls = mocker.patch("projet.app_init.ConfigLoader")
    mock_conf_cls.return_value.get_section.return_value = {
        'page_title': 'Test Title',
        'layout': 'wide'
    }

    AppInitializer.configure_page()

    mock_st.set_page_config.assert_called_once_with(
        page_title='Test Title',
        page_icon='🌡️',
        layout='wide'
    )

def test_setup_logging(mocker):
    mock_logging = mocker.patch("logging.basicConfig")
    mock_conf_cls = mocker.patch("projet.app_init.ConfigLoader")
    mock_conf_cls.return_value.get_section.return_value = {
        'level': 'DEBUG',
        'format': '%(message)s'
    }

    AppInitializer.setup_logging()

    mock_logging.assert_called_once()
    _, kwargs = mock_logging.call_args
    assert kwargs['level'] == 'DEBUG'

# --- Test init_services ---

def test_init_services(mocker):
    mocker.patch("projet.app_init.ConfigLoader")
    mocker.patch("projet.app_init.APIExtractor")
    mocker.patch("projet.app_init.DataValidator")
    mocker.patch("projet.app_init.ParquetHandler")
    mocker.patch("projet.app_init.DataFetcher")
    mocker.patch("projet.app_init.DataVizualiserFactory")

    res = AppInitializer.init_services()

    assert len(res) == 3
