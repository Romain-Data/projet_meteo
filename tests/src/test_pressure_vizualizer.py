import pandas as pd
import pytest

from projet.src.viz.pressure_vizualizer import PressureVizualizer

@pytest.fixture
def df_test_pressure():
    return pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01 10:00', '2023-01-01 11:00']),
        'pressure': [1013, 1015]
    })

def test_plot_calls_viz_utils_correctly(mocker, df_test_pressure):
    mock_create_chart = mocker.patch('projet.src.viz.pressure_vizualizer.viz_utils.create_time_series_chart')

    viz = PressureVizualizer()
    viz.plot(df_test_pressure)

    mock_create_chart.assert_called_once_with(
        df=df_test_pressure,
        y_col='pressure',
        title="Pressure Over Time",
        y_title="Pressure (Pa)",
        color='#2ca02c'
    )
