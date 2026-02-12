import logging
import numpy as np
import pandas as pd
import pytest

from projet.src.processing.validator import DataValidator

@pytest.fixture
def df_test():
    df_test = pd.DataFrame({
        'pressure': [85000, 101500],
        'humidity': [55, 60],
        'temperature': [20.5, 22.1],
        'date': pd.to_datetime(['2023-01-01', '2023-01-02'])
    })
    return df_test

@pytest.fixture
def validator():
    validation_rules = {
    "temperature": {
      "min": -20,
      "max": 60,
      "unit": "celsius"
    },
    "humidity": {
      "min": 0,
      "max": 100,
      "unit": "percent"
    },
    "pressure": {
      "min": 80000,
      "max": 110000,
      "unit": "Pa"
    }
  }
    validator = DataValidator(rules=validation_rules)
    return validator


def test_validator_initialization(validator):
    assert type(validator) == DataValidator
    assert type(validator.rules) == dict
    assert validator.rules['temperature']['max'] == 60


def test_is_format_correct():
    df_test = pd.DataFrame({
        'pressure': [1013, 1015],
        'humidity': [55, 60],
        'temperature': [20.5, 22.1],
        'date': pd.to_datetime(['2023-01-01', '2023-01-02'])
    })
    assert DataValidator({}).is_format_correct(df_test) == True


def test_is_format_correct_empty_dataframe(caplog):
    empty_df = pd.DataFrame()
    caplog.set_level(logging.WARNING)

    assert DataValidator({}).is_format_correct(empty_df) == False
    assert "Empty DataFrame provided for format validation" in caplog.text


@pytest.mark.parametrize("missing_column", ["pressure", "humidity", "temperature", "date"])
def test_is_format_correct_missing_column(caplog, df_test, missing_column):
    df = df_test.drop(columns=[missing_column])
    
    validator = DataValidator(rules={})
    caplog.set_level(logging.ERROR)

    assert validator.is_format_correct(df) is False
    assert f"Missing required column: {missing_column}" in caplog.text


def test_are_values_valid(validator, df_test):
    assert validator.are_values_valid(df_test) == True


def test_are_values_valid_limit(validator):
    df_limit = pd.DataFrame({
        'pressure': [110000],
        'humidity': [0],
        'temperature': [60],
        'date': pd.to_datetime(['2023-01-01'])
    })

    assert validator.are_values_valid(df_limit) == True


def test_are_values_valid_empty_df(validator, caplog):
    empty_df = pd.DataFrame()
    caplog.set_level(logging.WARNING)

    assert validator.are_values_valid(empty_df) == False
    assert "Empty DataFrame provided for value validation" in caplog.text


def test_are_values_valid_out_of_limit_down(validator, caplog):
    df_out_of_limit = pd.DataFrame({
        'pressure': [200],
        'humidity': [10],
        'temperature': [20],
        'date': pd.to_datetime(['2023-01-01'])
    })
    caplog.set_level(logging.ERROR)
    min = validator.rules['pressure']['min']
    max = validator.rules['pressure']['max']
    
    assert validator.are_values_valid(df_out_of_limit) == False
    assert f"Valeurs invalides dans pressure hors de l'intervalle [{min}, {max}]" in caplog.text


def test_are_values_valid_out_of_limit_up(validator, caplog):
    df_out_of_limit = pd.DataFrame({
        'pressure': [200000],
        'humidity': [10],
        'temperature': [20],
        'date': pd.to_datetime(['2023-01-01'])
    })
    caplog.set_level(logging.ERROR)
    min = validator.rules['pressure']['min']
    max = validator.rules['pressure']['max']
    
    assert validator.are_values_valid(df_out_of_limit) == False
    assert f"Valeurs invalides dans pressure hors de l'intervalle [{min}, {max}]" in caplog.text



def test_are_values_valid_missing_column_ignored(validator, df_test):
    df_missing = df_test.drop(columns=['pressure'])

    assert validator.are_values_valid(df_missing) is True


def test_is_format_correct_invalid_type(validator, df_test, caplog):
    df_invalid = df_test.copy()
    df_invalid['pressure'] = df_invalid['pressure'].astype(str)
    
    caplog.set_level(logging.ERROR)
    assert validator.is_format_correct(df_invalid) is False
    assert "Invalid type for pressure" in caplog.text


def test_is_format_correct_exception(validator, df_test, mocker):
    mocker.patch.object(pd.DataFrame, 'columns', new_callable=mocker.PropertyMock, side_effect=Exception("Erreur inattendue"))
    
    assert validator.is_format_correct(df_test) is False


def test_are_values_valid_exception(validator, df_test, mocker):
    # On simule une erreur inattendue lors de la validation des valeurs
    mocker.patch.object(pd.Series, 'between', side_effect=Exception("Erreur inattendue"))
    
    assert validator.are_values_valid(df_test) is False