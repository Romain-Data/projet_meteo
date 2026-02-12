import pandas as pd
import pytest
from datetime import datetime, timedelta

from projet.src.viz.data_vizualizer_factory import DataVizualiserFactory


@pytest.fixture
def factory():
    return DataVizualiserFactory()

@pytest.fixture
def mixed_date_df():
    """DataFrame avec des dates récentes (< 7 jours) et anciennes (> 7 jours)"""
    now = datetime.now()
    return pd.DataFrame({
        'date': [
            now - timedelta(days=1),  # Récent
            now - timedelta(days=5),  # Récent
            now - timedelta(days=8),  # Trop vieux
            now - timedelta(days=365) # Trop vieux
        ],
        'temperature': [10, 11, 12, 13],
        'humidity': [50, 51, 52, 53],
        'pressure': [1000, 1001, 1002, 1003]
    })

def test_plot_temperature_dispatch(factory, mixed_date_df, mocker):
    mock_viz = mocker.patch('projet.src.viz.data_vizualizer_factory.TemperatureVizualizer')
    mock_instance = mock_viz.return_value
    
    factory.plot("temperature", mixed_date_df)
    
    mock_viz.assert_called_once()
    mock_instance.plot.assert_called_once()
    
    args, _ = mock_instance.plot.call_args
    filtered_df = args[0]
    assert len(filtered_df) == 2
    assert filtered_df['temperature'].tolist() == [10, 11]

def test_plot_humidity_dispatch(factory, mixed_date_df, mocker):
    mock_viz = mocker.patch('projet.src.viz.data_vizualizer_factory.HumidityVizualizer')
    mock_instance = mock_viz.return_value
    
    factory.plot("humidity", mixed_date_df)
    
    mock_viz.assert_called_once()
    mock_instance.plot.assert_called_once()

def test_plot_pressure_dispatch(factory, mixed_date_df, mocker):
    mock_viz = mocker.patch('projet.src.viz.data_vizualizer_factory.PressureVizualizer')
    mock_instance = mock_viz.return_value
    
    factory.plot("pressure", mixed_date_df)
    
    mock_viz.assert_called_once()
    mock_instance.plot.assert_called_once()

def test_plot_invalid_type_raises_value_error(factory, mixed_date_df):
    with pytest.raises(ValueError) as exc_info:
        factory.plot("unknown_type", mixed_date_df)
    
    assert "Invalid mesure_type: unknown_type" in str(exc_info.value)

def test_plot_converts_string_dates(factory, mocker):
    row_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    df_str_dates = pd.DataFrame({
        'date': [row_date],
        'temperature': [15]
    })
    
    mock_viz = mocker.patch('projet.src.viz.data_vizualizer_factory.TemperatureVizualizer')
    mock_instance = mock_viz.return_value
    
    factory.plot("temperature", df_str_dates)
    
    args, _ = mock_instance.plot.call_args
    filtered_df = args[0]
    assert pd.api.types.is_datetime64_any_dtype(filtered_df['date'])
    assert len(filtered_df) == 1

def test_plot_handles_timezone_aware_dates(factory, mocker):
    now_utc = pd.Timestamp.now(tz='UTC')
    df_tz = pd.DataFrame({
        'date': [now_utc - pd.Timedelta(days=1), now_utc - pd.Timedelta(days=10)],
        'temperature': [20, 21]
    })
    
    mock_viz = mocker.patch('projet.src.viz.data_vizualizer_factory.TemperatureVizualizer')
    mock_instance = mock_viz.return_value
    
    factory.plot("temperature", df_tz)
    
    args, _ = mock_instance.plot.call_args
    filtered_df = args[0]
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]['temperature'] == 20
