import pandas as pd
import pytest
import plotly.graph_objects as go
from projet.src.viz import viz_utils

@pytest.fixture
def df_test():
    return pd.DataFrame({
        'date': pd.to_datetime(['2023-01-01 10:00', '2023-01-01 11:00', '2023-01-02 10:00']),
        'temperature': [10, 12, 11],
        'humidity': [50, 55, 60]
    })

def test_create_line_trace(df_test):
    trace = viz_utils.create_line_trace(
        df=df_test,
        x_col='date',
        y_col='temperature',
        name='Temp',
        color='#FF0000'
    )
    
    assert isinstance(trace, go.Scatter)
    assert trace.name == 'Temp'
    assert trace.mode == 'lines+markers'
    assert trace.line.color == '#FF0000'
    assert list(trace.x) == list(df_test['date'])
    assert list(trace.y) == list(df_test['temperature'])

def test_create_date_change_annotations(df_test):
    annotations = viz_utils.create_date_change_annotations(df_test)
    
    # Il y a un changement de date entre l'index 1 (01 jan) et 2 (02 jan)
    assert len(annotations) == 1
    ann = annotations[0]
    assert ann['text'] == '02 January' or ann['text'] == '02 janvier'
    assert ann['x'] == df_test['date'].iloc[2]
    assert ann['yshift'] == -53  # Test de décalage de label 

def test_create_date_change_annotations_no_change():
    df = pd.DataFrame({'date': pd.to_datetime(['2023-01-01 10:00', '2023-01-01 11:00'])})
    annotations = viz_utils.create_date_change_annotations(df)
    assert len(annotations) == 0

def test_update_layout(mocker):
    fig = mocker.Mock(spec=go.Figure)
    annotations = [{'text': 'test'}]
    
    viz_utils.update_layout(fig, "Title", "Y Axis", annotations)
    
    fig.update_layout.assert_called_once()
    call_args = fig.update_layout.call_args[1]
    
    assert call_args['title']['text'] == "Title"
    assert call_args['yaxis']['title'] == "Y Axis"
    assert call_args['annotations'] == annotations
    assert call_args['plot_bgcolor'] == 'white'

def test_create_time_series_chart_nominal(df_test, mocker):
    spy_trace = mocker.spy(viz_utils, 'create_line_trace')
    spy_annot = mocker.spy(viz_utils, 'create_date_change_annotations')
    spy_layout = mocker.spy(viz_utils, 'update_layout')
    
    fig = viz_utils.create_time_series_chart(
        df=df_test,
        y_col='temperature',
        title="My Chart",
        y_title="Temp (C)",
        color="red"
    )
    
    assert isinstance(fig, go.Figure)
    # Vérifie que les sous-fonctions ont été appelées
    spy_trace.assert_called_once()
    spy_annot.assert_called_once()
    spy_layout.assert_called_once()
    # Vérifie que la figure contient bien une trace
    assert len(fig.data) == 1
    assert fig.data[0].name == "Temp (C)"

def test_create_time_series_chart_empty(caplog):
    empty_df = pd.DataFrame()
    fig = viz_utils.create_time_series_chart(
        df=empty_df, y_col='temp', title='T', y_title='Y', color='red'
    )
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 0 # Figure vide
    assert "Cannot create chart: empty DataFrame" in caplog.text

def test_create_time_series_chart_exception(df_test, mocker, caplog):
    mocker.patch('projet.src.viz.viz_utils.create_line_trace', side_effect=Exception("Erreur innatendue"))
    
    fig = viz_utils.create_time_series_chart(
        df=df_test, y_col='temperature', title='T', y_title='Y', color='red'
    )
    
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 0
    assert "Chart creation failed: Exception - Erreur innatendue" in caplog.text
