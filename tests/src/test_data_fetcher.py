import pandas as pd
import pytest
from projet.src.services.data_fetcher import DataFetcher


# FIXTURES (Mocks)

@pytest.fixture
def mock_extractor(mocker):
    return mocker.patch('projet.src.api.extractor.APIExtractor')

@pytest.fixture
def mock_transformer(mocker):
    return mocker.patch('projet.src.processing.transformer.DataTransformer')

@pytest.fixture
def mock_validator(mocker):
    return mocker.patch('projet.src.processing.validator.DataValidator')

@pytest.fixture
def mock_loader(mocker):
    return mocker.patch('projet.src.services.loader.DataLoader')

@pytest.fixture
def mock_parquet_handler(mocker):
    return mocker.patch('projet.src.storage.parquet_handler.ParquetHandler')

@pytest.fixture
def mock_station(mocker):
    station = mocker.Mock(name="Station")
    station.name = "TestStation"
    return station

@pytest.fixture
def fetcher(mock_extractor, mock_transformer, mock_validator, mock_loader, mock_parquet_handler):
    # On instancie DataFetcher avec nos mocks
    return DataFetcher(
        extractor=mock_extractor,
        transformer=mock_transformer,
        validator=mock_validator,
        loader=mock_loader,
        parquet_handler=mock_parquet_handler
    )

# TESTS

def test_fetch_and_load_success(fetcher, mock_extractor, mock_transformer, mock_validator, mock_loader, mock_station):
    """Test Nominal : Tout se passe bien (Extract -> Transform -> Validate -> Load)"""
    
    # Extract renvoie un DataFrame non vide
    mock_extractor.extract.return_value = pd.DataFrame({'raw': [1]})
    
    # Transform renvoie un DataFrame formaté
    formatted_df = pd.DataFrame({'clean': [1]})
    mock_transformer.format_data.return_value = formatted_df
    mock_transformer.normalize_columns.return_value = formatted_df
    
    # Validate renvoie True
    mock_validator.is_format_correct.return_value = True
    mock_validator.are_values_valid.return_value = True
    
    # 2. Appel de la fonction
    result = fetcher.fetch_and_load(mock_station)
    
    # 3. Vérifications
    assert result is True
    
    # Vérifie que chaque étape a été appelée
    mock_extractor.extract.assert_called_once_with(mock_station)
    mock_transformer.format_data.assert_called_once()
    mock_transformer.normalize_columns.assert_called_once()
    mock_validator.is_format_correct.assert_called_once()
    mock_validator.are_values_valid.assert_called_once()
    mock_loader.load_reports.assert_called_once_with(mock_station, formatted_df)

def test_fetch_and_load_empty_data(fetcher, mock_extractor, mock_station):
    """Test : L'extraction ne renvoie aucune donnée"""
    
    # Extract renvoie un DataFrame vide
    mock_extractor.extract.return_value = pd.DataFrame()
    
    result = fetcher.fetch_and_load(mock_station)
    
    assert result is False
    # Vérifie qu'on s'arrête là et qu'on n'appelle pas la suite
    fetcher.transformer.format_data.assert_not_called()

def test_fetch_and_load_invalid_format(fetcher, mock_extractor, mock_transformer, mock_validator, mock_station):
    """Test : Le format des données est invalide après transformation"""
    
    mock_extractor.extract.return_value = pd.DataFrame({'raw': [1]})
    mock_transformer.format_data.return_value = pd.DataFrame({'clean': [1]})
    mock_transformer.normalize_columns.return_value = pd.DataFrame({'clean': [1]})
    
    # Validation format échoue
    mock_validator.is_format_correct.return_value = False
    
    result = fetcher.fetch_and_load(mock_station)
    
    assert result is False
    # Vérifie qu'on ne charge pas les données
    fetcher.loader.load_reports.assert_not_called()

def test_fetch_and_load_invalid_values(fetcher, mock_extractor, mock_transformer, mock_validator, mock_station):
    """Test : Les valeurs sont invalides (ex: température > 60°C)"""
    
    mock_extractor.extract.return_value = pd.DataFrame({'raw': [1]})
    # On doit simuler les retours des transformers sinon ça plante si le code les utilise
    formatted_df = pd.DataFrame({'clean': [1]})
    mock_transformer.format_data.return_value = formatted_df
    mock_transformer.normalize_columns.return_value = formatted_df
    
    mock_validator.is_format_correct.return_value = True
    # Validation valeurs échoue
    mock_validator.are_values_valid.return_value = False
    
    result = fetcher.fetch_and_load(mock_station)
    
    assert result is False
    fetcher.loader.load_reports.assert_not_called()

def test_refresh_and_save_success(fetcher, mock_station, mock_parquet_handler, mocker):
    """Test Pipeline Complete : Fetch & Load OK -> Save OK"""
    
    mocker.patch.object(fetcher, 'fetch_and_load', return_value=True)
    
    mock_parquet_handler.save_station_reports.return_value = True
    
    result = fetcher.refresh_and_save_station_data(mock_station)
    
    assert result is True
    fetcher.fetch_and_load.assert_called_once_with(mock_station)
    mock_parquet_handler.save_station_reports.assert_called_once_with(mock_station)

def test_refresh_and_save_fetch_fail(fetcher, mock_station, mock_parquet_handler, mocker):
    """Test : Echec lors du Fetch"""
    
    mocker.patch.object(fetcher, 'fetch_and_load', return_value=False)
    
    result = fetcher.refresh_and_save_station_data(mock_station)
    
    assert result is False
    # Vérifie qu'on n'essaie pas de sauvegarder si le fetch a échoué
    mock_parquet_handler.save_station_reports.assert_not_called()

def test_refresh_and_save_save_fail(fetcher, mock_station, mock_parquet_handler, mocker):
    """Test : Fetch OK mais Echec de la Sauvegarde"""
    
    mocker.patch.object(fetcher, 'fetch_and_load', return_value=True)
    mock_parquet_handler.save_station_reports.return_value = False
    
    result = fetcher.refresh_and_save_station_data(mock_station)
    
    assert result is False
