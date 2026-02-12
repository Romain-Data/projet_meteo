import pandas as pd
import pytest
from pathlib import Path

from projet.src.storage.parquet_handler import ParquetHandler
from projet.src.entities.station import Station
from projet.src.entities.weather_report import WeatherReport


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture pour créer un répertoire temporaire"""
    return tmp_path / "data" / "parquet"

@pytest.fixture
def handler(temp_dir):
    """Fixture pour instancier ParquetHandler avec un répertoire temporaire"""
    return ParquetHandler(data_dir=temp_dir)

@pytest.fixture
def station():
    return Station(1, "Test Station", 0, 0)

@pytest.fixture
def test_reports():
    return [
        WeatherReport(pd.to_datetime("2023-01-01 12:00"), 10, 50, 1013, "01 Jan"),
        WeatherReport(pd.to_datetime("2023-01-02 12:00"), 12, 55, 1015, "02 Jan")
    ]

def test_init_creates_directory(temp_dir):
    ParquetHandler(data_dir=temp_dir)
    assert temp_dir.exists()

def test_init_default_directory(mocker):
    mock_path = mocker.patch('projet.src.storage.parquet_handler.Path')
    mock_parent = mock_path.return_value.parent.parent.parent
    
    ParquetHandler()
    
    # Vérifie que le chemin par défaut est bien construit
    assert mock_parent.__truediv__.called

def test_save_station_reports_new_file(handler, station, test_reports):
    station.reports = test_reports
    handler.save_station_reports(station)
    
    filepath = handler._get_filepath(station)
    assert filepath.exists()
    
    df = pd.read_parquet(filepath)
    assert len(df) == 2
    assert df.iloc[0]['temperature'] == 10

def test_save_station_reports_no_reports(handler, station, caplog):
    station.reports = []
    handler.save_station_reports(station)
    
    filepath = handler._get_filepath(station)
    assert not filepath.exists()
    assert "No reports to save" in caplog.text

def test_save_station_reports_merge(handler, station, test_reports):
    """Test le merge de deux fichiers"""
    station.reports = [test_reports[0]]
    handler.save_station_reports(station)
    
    station.reports = [test_reports[1]]
    handler.save_station_reports(station)
    
    filepath = handler._get_filepath(station)
    df = pd.read_parquet(filepath)
    assert len(df) == 2
    df = df.sort_values('date')
    assert df.iloc[0]['temperature'] == 10
    assert df.iloc[1]['temperature'] == 12

def test_load_station_reports(handler, station, test_reports):
    """Test le chargement des rapports"""
    station.reports = test_reports
    handler.save_station_reports(station)
    
    station.reports = []
    
    handler.load_station_reports(station)
    
    assert len(station.reports) == 2
    assert station.reports[0].temperature == 10

def test_load_station_reports_missing_file(handler, station, caplog):
    handler.load_station_reports(station)
    
    assert len(station.reports) == 0
    assert "No parquet file found" in caplog.text

def test_station_file_exists(handler, station, test_reports):
    assert not handler.station_file_exists(station)
    
    station.reports = test_reports
    handler.save_station_reports(station)
    
    assert handler.station_file_exists(station)

def test_save_error_handling(handler, station, test_reports, mocker, caplog):
    station.reports = test_reports
    mocker.patch('pandas.DataFrame.to_parquet', side_effect=Exception("Disk full"))
    
    with pytest.raises(Exception):
        handler.save_station_reports(station)
    
    assert "Failed to save reports" in caplog.text

def test_load_error_handling(handler, station, mocker, caplog):
    mocker.patch('pandas.read_parquet', side_effect=Exception("Fichier corrompu"))
    mocker.patch('pathlib.Path.exists', return_value=True)
    
    handler.load_station_reports(station)
    
    assert len(station.reports) == 0
    assert "Failed to load reports" in caplog.text

def test_merge_error_handling(handler, station, test_reports, caplog):
    """Test le merge de deux fichiers"""
    from unittest.mock import patch
    
    station.reports = [test_reports[0]]
    handler.save_station_reports(station)
    
    with patch('pandas.read_parquet', side_effect=Exception("Fichier corrompu")):
        station.reports = [test_reports[1]]
        handler.save_station_reports(station)
    
    assert "Failed to read existing file" in caplog.text
    
    filepath = handler._get_filepath(station)
    df = pd.read_parquet(filepath)
    assert len(df) == 1
    assert df.iloc[0]['temperature'] == 12
