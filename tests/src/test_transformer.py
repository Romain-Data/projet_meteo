import numpy as np
import pandas as pd
import pytest

from projet.src.processing.transformer import DataTransformer

@pytest.fixture
def transformer():
    return DataTransformer()

def test_format_data_nominal(transformer):
    """Test Nominal : Transformation OK (dates, types)"""
    # DataFrame brut simulé (sortie API)
    raw_df = pd.DataFrame({
        'heure_de_paris': ['01/01/2023 12h'],
        'temperature_en_degre_c': ['10.5'],
        'humidite': ['80'],
        'pression': ['1013']
    })
    
    result_df = transformer.format_data(raw_df)
    
    assert not result_df.empty
    assert 'display_date' in result_df.columns
    assert result_df['display_date'].iloc[0] == '2023-01-01 12:00'
    assert result_df['temperature_en_degre_c'].dtype == np.float64
    assert result_df['humidite'].dtype == np.int64
    assert result_df['pression'].dtype == np.int64

def test_format_data_empty(transformer):
    result_df = transformer.format_data(pd.DataFrame())
    assert result_df.empty

def test_format_data_missing_date_column(transformer):
    """Test : Colonne 'heure_de_paris' manquante renvoie DataFrame vide"""
    # Pas de colonne 'heure_de_paris'
    raw_df = pd.DataFrame({'temp': [10]})
    result_df = transformer.format_data(raw_df)
    assert result_df.empty

def test_format_data_conversion_error(transformer):
    """Test : Erreur de conversion (ex: date invalide) renvoie DataFrame vide"""
    # Date impossible à parser
    raw_df = pd.DataFrame({
        'heure_de_paris': ['Not a date'],
        'temperature_en_degre_c': ['10'],
        'humidite': ['80'],
        'pression': ['1013']
    })
    result_df = transformer.format_data(raw_df)
    assert result_df.empty


def test_normalize_columns_nominal(transformer):
    """Test : Renommage des colonnes API vers format interne"""
    # Colonnes API
    df = pd.DataFrame({
        'heure_de_paris': [pd.Timestamp('2023-01-01 12:00:00')],
        'temperature_en_degre_c': [10.5],
        'humidite': [80],
        'pression': [1013]
    })
    
    result_df = transformer.normalize_columns(df)
    
    expected_cols = ['date', 'temperature', 'humidity', 'pressure', 'display_date']
    for col in expected_cols:
        assert col in result_df.columns

def test_normalize_columns_already_normalized(transformer):
    """Test : Colonnes déjà correctes restent inchangées"""
    df = pd.DataFrame({
        'date': [pd.Timestamp('2023-01-01')],
        'temperature': [10],
        'humidity': [50],
        'pressure': [1000]
    })
    
    result_df = transformer.normalize_columns(df)
    
    assert 'date' in result_df.columns
    assert 'temperature' in result_df.columns
    assert 'display_date' in result_df.columns

def test_normalize_columns_generates_display_date(transformer):
    """Test : Génération de display_date si absente"""
    df = pd.DataFrame({
        'date': [pd.Timestamp('2023-01-01 14:30:00')]
    })
    
    result_df = transformer.normalize_columns(df)
    
    assert result_df['display_date'].iloc[0] == '2023-01-01 14:30:00'
