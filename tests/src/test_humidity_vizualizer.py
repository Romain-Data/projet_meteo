import pandas as pd
import pytest

from projet.src.viz.humidity_vizualizer import HumidityVizualizer

@pytest.fixture
def df_test_humidity():
    return pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01 10:00', '2023-01-01 11:00']),
        'humidity': [45, 50]
    })

def test_plot_calls_viz_utils_correctly(mocker, df_test_humidity):
    mock_create_chart = mocker.patch('projet.src.viz.humidity_vizualizer.viz_utils.create_time_series_chart')

    viz = HumidityVizualizer()
    viz.plot(df_test_humidity)

    mock_create_chart.assert_called_once_with(
        df=df_test_humidity,
        y_col='humidity',
        title="Humidity Over Time",
        y_title="Humidity (%)",
        color='#1f77b4'
    )
