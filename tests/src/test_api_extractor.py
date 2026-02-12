import pandas as pd
import pytest
import requests
from projet.src.api.extractor import APIExtractor

@pytest.fixture
def mock_station(mocker):
    station = mocker.Mock(name="Station")
    station.name = "Toulouse-Blagnac"
    station.id = "toulouse-blagnac"
    return station

@pytest.fixture
def extractor():
    return APIExtractor()

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch('requests.get')

def test_extract_success(extractor, mock_station, mock_requests_get):
    """Test Nominal : Extraction réussie avec des données"""
    # Mock de la réponse API
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'results': [
            {'heure_de_paris': '2023-01-01 12:00', 'temp': 15},
            {'heure_de_paris': '2023-01-01 13:00', 'temp': 16}
        ]
    }
    
    df = extractor.extract(mock_station)
    
    # Vérifications
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'heure_de_paris' in df.columns
    
    # Vérifie l'appel requests
    mock_requests_get.assert_called_once()
    args, kwargs = mock_requests_get.call_args
    assert "toulouse-blagnac/records" in args[0]
    assert kwargs['params']['limit'] == '100'

def test_extract_no_results_key(extractor, mock_station, mock_requests_get):
    """Test : API répond mais sans clé 'results'"""
    mock_response = mock_requests_get.return_value
    mock_response.json.return_value = {'error': 'Something went wrong'}
    
    df = extractor.extract(mock_station)
    
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_extract_empty_results(extractor, mock_station, mock_requests_get):
    """Test : API répond avec une liste vide dans 'results'"""
    mock_response = mock_requests_get.return_value
    mock_response.json.return_value = {'results': []}
    
    df = extractor.extract(mock_station)
    
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_extract_request_exception(extractor, mock_station, mock_requests_get):
    """Test : Erreur réseau (timeout, connection error, etc.)"""
    mock_requests_get.side_effect = requests.exceptions.RequestException("Timeout")
    
    df = extractor.extract(mock_station)
    
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_extract_http_error(extractor, mock_station, mock_requests_get):
    """Test : Erreur HTTP (404, 500) via raise_for_status"""
    mock_response = mock_requests_get.return_value
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    
    df = extractor.extract(mock_station)
    
    assert isinstance(df, pd.DataFrame)
    assert df.empty
