"""
Ce fichier, c'est uniquement pour flex avec une couverture à 100%
Je ne comprends pas vraiment les tests qui sont réalisés ici

Mock Streamilt devient trop Meta pour moi 
"""

import pandas as pd
import pytest
import streamlit as st
import runpy

from projet.app import main, _render_dashboard

class SessionStateMock(dict):
    """Simule st.session_state avec support du format dictionnaire et attributs."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"SessionState has no attribute {key}")
    
    def __setattr__(self, key, value):
        self[key] = value

@pytest.fixture
def mock_st(mocker):
    state = SessionStateMock()
    # Initialisation des états par défaut pour éviter les KeyError
    state['task_status'] = {"refresh_needed": False}
    
    mocker.patch.object(st, "session_state", state)
    mocker.patch.object(st, "rerun")
    mocker.patch.object(st, "sidebar")
    mocker.patch.object(st, "header")
    mocker.patch.object(st, "selectbox")
    mocker.patch.object(st, "plotly_chart")
    mocker.patch.object(st, "spinner")
    # Patch time.sleep pour accélérer les tests
    mocker.patch("time.sleep")
    return st

@pytest.fixture
def mock_components(mocker):
    mocks = {
        "ConfigLoader": mocker.patch("projet.app.ConfigLoader"),
        "AppInitializer": mocker.patch("projet.app.AppInitializer"),
        "ApiRequestQueue": mocker.patch("projet.app.ApiRequestQueue"),
        "LinkedListNavigator": mocker.patch("projet.app.LinkedListNavigator"),
        "Sidebar": mocker.patch("projet.app.Sidebar"),
        "NavigationHeader": mocker.patch("projet.app.NavigationHeader"),
        "MetricsDisplay": mocker.patch("projet.app.MetricsDisplay")
    }
    # Forçage du retour de init_services pour l'unpacking (important !)
    mock_init_instance = mocks["AppInitializer"].return_value
    mock_init_instance.init_services.return_value = (mocker.Mock(), mocker.Mock(), mocker.Mock())
    return mocks

def test_main_initialization_flow(mocker, mock_st, mock_components):
    # Setup pour passer les étapes de navigation
    mock_init = mock_components["AppInitializer"].return_value
    mock_station = mocker.Mock(id="S1", name="Station Test")
    mock_init.load_stations.return_value = [mock_station]
    
    # Simuler le fait que les objets ne sont pas encore en session
    # (On vide le dictionnaire initialisé par la fixture)
    st.session_state.clear()
    st.session_state.task_status = {"refresh_needed": False}

    main()

    # Vérifications
    assert "api_queue" in st.session_state
    assert "navigator" in st.session_state
    mock_components["ApiRequestQueue"].called

def test_main_rerun_when_api_working(mocker, mock_st, mock_components):
    # Setup : simuler une file d'attente qui travaille
    mock_queue = mocker.Mock()
    mock_queue.is_working = True
    st.session_state.api_queue = mock_queue
    st.session_state.task_status = {"refresh_needed": False}

    main()
    
    # Vérifie que le code appelle rerun à cause de is_working
    assert st.rerun.called

def test_render_dashboard_normal_metric(mocker, mock_st):
    # Mock des données de station
    mock_station = mocker.Mock()
    df_mock = pd.DataFrame({'temperature': [20]})
    mock_station.get_all_reports.return_value = df_mock
    
    mock_latest = mocker.Mock()
    mock_latest.display_date = "2023-01-01"
    mock_station.get_latest_reports.return_value = mock_latest
    
    mock_charts = mocker.Mock()
    st.selectbox.return_value = "Temperature"
    
    mocker.patch.object(st, "caption")

    _render_dashboard(mock_station, mock_charts)

    # Vérification des appels graphiques
    assert st.plotly_chart.called
    mock_charts.plot.assert_called_once()

def test_render_dashboard_no_reports(mocker, mock_st):
    # Test du cas où les rapports sont vides
    mock_station = mocker.Mock()
    mock_station.get_all_reports.return_value = pd.DataFrame() # Vide
    
    mock_latest = mocker.Mock()
    mock_latest.display_date = "N/A"
    mock_station.get_latest_reports.return_value = mock_latest
    
    mocker.patch.object(st, "info")
    st.selectbox.return_value = "Temperature"

    _render_dashboard(mock_station, mocker.Mock())

    st.info.assert_called_with("Not enough data to display chart")

def test_main_refresh_needed(mocker, mock_st, mock_components):
    # Setup : simuler un besoin de rafraîchissement
    st.session_state.task_status = {"refresh_needed": True}
    st.session_state.api_queue = mocker.Mock(is_working=False)
    st.session_state.navigator = mocker.Mock()
    
    main()
    
    assert st.session_state.task_status["refresh_needed"] is False
    assert st.rerun.called

def test_render_dashboard_surprise(mocker, mock_st):
    mock_station = mocker.Mock()
    st.selectbox.return_value = "Surprise 🎁"
    mocker.patch.object(st, "video")
    
    _render_dashboard(mock_station, mocker.Mock())
    
    assert st.video.called

def test_main_no_data_available(mocker, mock_st, mock_components):
    # Setup : simuler une station sans données
    st.session_state.task_status = {"refresh_needed": False}
    st.session_state.api_queue = mocker.Mock(is_working=False)
    
    mock_station = mocker.Mock()
    mock_station.reports = False # Simule if not current_station.reports
    
    mock_nav = mocker.Mock()
    mock_nav.get_current.return_value = mock_station
    st.session_state.navigator = mock_nav
    
    # Mock config
    mock_components["ConfigLoader"].return_value.get.return_value = "Title"
    mocker.patch.object(st, "warning")
    main()

    assert st.warning.called

def test_script_execution_entry_point_via_side_effect(mocker):
    # Au lieu de mocker main (qui est redéfini par runpy), 
    # on mock ce que main APPELLE en premier.
    mock_setup = mocker.patch("projet.app.AppInitializer.setup_logging")
    
    # On mock aussi les autres composants pour éviter que le reste du script ne plante
    mocker.patch("projet.app.ConfigLoader")

    try:
        runpy.run_path("projet/app.py", run_name="__main__")
    except Exception:
        pass

    # Si setup_logging a été appelé, c'est que le bloc if __name__ == "__main__": 
    # a bien exécuté main()
    assert mock_setup.called
