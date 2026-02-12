import pandas as pd
import pytest

from projet.src.viz.temperature_vizualizer import TemperatureVizualizer

@pytest.fixture
def df_test():
    return pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01 10:00', '2023-01-01 11:00']),
        'temperature': [20.5, 22.1]
    })

def test_plot_calls_viz_utils_correctly(mocker, df_test):
    mock_create_chart = mocker.patch('projet.src.viz.temperature_vizualizer.viz_utils.create_time_series_chart')

    viz = TemperatureVizualizer()
    viz.plot(df_test)

    mock_create_chart.assert_called_once_with(
        df=df_test,
        y_col='temperature',
        title="Temperature Over Time",
        y_title="Temperature (°C)",
        color='#FB8500'
    )