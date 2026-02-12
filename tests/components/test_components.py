import pytest
import pandas as pd
from unittest.mock import MagicMock
from projet.components.metrics_display import MetricsDisplay
from projet.components.navigation_header import NavigationHeader
from projet.components.sidebar import Sidebar

# --- Fixtures ---

@pytest.fixture
def mock_streamlit(mocker):
    # Patch all st usages
    mock_metrics = mocker.patch("projet.components.metrics_display.st")
    mock_header = mocker.patch("projet.components.navigation_header.st")
    mock_sidebar = mocker.patch("projet.components.sidebar.st")
    return mock_metrics, mock_header, mock_sidebar

@pytest.fixture
def mock_navigator(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_api_queue(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_data_fetcher(mocker):
    return mocker.Mock()

@pytest.fixture
def mock_parquet_handler(mocker):
    return mocker.Mock()


# --- MetricsDisplay Tests ---

def test_render_statistics(mocker):
    """Test : Calcul et affichage des statistiques"""
    mock_st = mocker.patch("projet.components.metrics_display.st")
    
    # Mock expander (context manager)
    mock_expander = mocker.MagicMock()
    mock_st.expander.return_value.__enter__.return_value = mock_expander
    
    # Mock columns (context managers for each column)
    mock_col1 = mocker.MagicMock()
    mock_col2 = mocker.MagicMock()
    mock_col3 = mocker.MagicMock()
    mock_st.columns.return_value = [mock_col1, mock_col2, mock_col3]
    
    # Make columns context managers too
    mock_col1.__enter__.return_value = mock_col1
    mock_col2.__enter__.return_value = mock_col2
    mock_col3.__enter__.return_value = mock_col3
    
    df = pd.DataFrame({'temperature': [10, 20, 30]})
    
    MetricsDisplay.render_statistics(df)
    
    mock_st.expander.assert_called_once_with("📈 Statistics")
    mock_st.columns.assert_called_once_with(3)
    assert mock_st.metric.call_count == 3


# --- NavigationHeader Tests ---

def test_navigation_header_render_previous(mocker, mock_navigator, mock_api_queue, mock_data_fetcher):
    """Test : Navigation vers la station précédente"""
    mock_st = mocker.patch("projet.components.navigation_header.st")
    
    # Mock columns with context manager support
    c1, c2, c3 = mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock()
    c1.__enter__.return_value = c1
    c3.__enter__.return_value = c3
    mock_st.columns.return_value = [c1, c2, c3]
    
    # Mock session_state as an object allowing attribute assignment
    # Use a real dict for underlying storage but access via attributes (Mock)
    mock_st.session_state = mocker.MagicMock()
    
    # Simulate Previous button clicked
    mock_st.button.side_effect = lambda label, **kwargs: label == "← Previous"
    
    prev_station = mocker.Mock(id=123)
    mock_navigator.get_previous.return_value = prev_station
    
    NavigationHeader.render(mock_navigator, mock_api_queue, mock_data_fetcher)
    
    # Verify assignment to session_state
    assert mock_st.session_state.selected_station_id == 123
    mock_api_queue.add_task.assert_called_once()
    mock_st.rerun.assert_called_once()

def test_navigation_header_render_next(mocker, mock_navigator, mock_api_queue, mock_data_fetcher):
    """Test : Navigation vers la station suivante"""
    mock_st = mocker.patch("projet.components.navigation_header.st")
    
    c1, c2, c3 = mocker.MagicMock(), mocker.MagicMock(), mocker.MagicMock()
    c1.__enter__.return_value = c1
    c3.__enter__.return_value = c3
    mock_st.columns.return_value = [c1, c2, c3]
    
    mock_st.session_state = mocker.MagicMock()
    
    # Simulate Next button clicked
    mock_st.button.side_effect = lambda label, **kwargs: label == "Next →"
    
    next_station = mocker.Mock(id=456)
    mock_navigator.get_next.return_value = next_station
    
    NavigationHeader.render(mock_navigator, mock_api_queue, mock_data_fetcher)
    
    assert mock_st.session_state.selected_station_id == 456
    mock_api_queue.add_task.assert_called_once()
    mock_st.rerun.assert_called_once()


# --- Sidebar Tests ---

def test_sidebar_render(mocker, mock_parquet_handler, mock_data_fetcher, mock_api_queue, mock_navigator):
    """Test : Rendu de la sidebar et sélection"""
    mock_st = mocker.patch("projet.components.sidebar.st")
    
    # Mock sidebar context manager
    mock_st.sidebar.__enter__.return_value = mock_st.sidebar
    
    # Mock data
    s1 = mocker.Mock(id="s1", name="Station 1")
    s2 = mocker.Mock(id="s2", name="Station 2")
    
    mock_navigator.get_all_stations.return_value = [s1, s2]
    mock_navigator.get_current.return_value = s1
    
    # Mock session state (dict-like for get, attribute-like for set)
    # Sidebar uses st.session_state.get() AND st.session_state.selected_station_id = ...
    # So we need a hybrid mock. Wrapper around a dict is easiest.
    session_dict = {'selected_station_id': 's1'}
    mock_st.session_state.get.side_effect = session_dict.get
    mock_st.session_state.__getitem__.side_effect = session_dict.__getitem__
    mock_st.session_state.__setitem__.side_effect = session_dict.__setitem__
    # Also support attribute assignment for eventual consistency if code changes
    
    # Mock selectbox to return s2
    mock_st.selectbox.return_value = "s2"
    
    # Ensure refresh button is NOT clicked (default mock is truthy)
    mock_st.button.return_value = False
    
    sidebar = Sidebar(mock_parquet_handler, mock_data_fetcher, mock_api_queue)
    
    # Render
    sidebar.render(mock_navigator)
    
    # Verify s2 was set
    mock_navigator.set_current.assert_called_once_with(s2)
    # Verify session state update (Sidebar uses direct assignment st.session_state.selected_station_id = ...)
    # Wait, Sidebar code: st.session_state.selected_station_id = selected_station.id
    # If we mock session_state as a MagicMock, we can check attribute assignment.
    # But Sidebar ALSO uses .get().
    # Let's verify via the mock calls for assignment.
    assert mock_st.session_state.selected_station_id == "s2"
    
    mock_api_queue.add_task.assert_called_once()
    mock_st.rerun.assert_called_once()

def test_sidebar_refresh_button(mocker, mock_parquet_handler, mock_data_fetcher, mock_api_queue, mock_navigator):
    """Test : Clic sur le bouton refresh"""
    mock_st = mocker.patch("projet.components.sidebar.st")
    mock_st.sidebar.__enter__.return_value = mock_st.sidebar
    
    s1 = mocker.Mock(id="s1", name="Station 1")
    mock_navigator.get_all_stations.return_value = [s1]
    mock_navigator.get_current.return_value = s1
    
    # Setup session state .get
    mock_st.session_state.get.return_value = 's1'
    
    # Selectbox returns s1
    mock_st.selectbox.return_value = "s1"
    
    # Button "Refresh" clicked
    mock_st.button.return_value = True
    
    sidebar = Sidebar(mock_parquet_handler, mock_data_fetcher, mock_api_queue)
    sidebar.render(mock_navigator)
    
    mock_api_queue.add_task.assert_called_once()
    mock_st.toast.assert_called_once()
    mock_st.rerun.assert_called_once()

def test_sidebar_render_fallback_when_id_not_found(mocker, mock_parquet_handler, mock_data_fetcher, mock_api_queue, mock_navigator):
    """Test : Fallback sur la première station si l'ID en session n'existe plus"""
    mock_st = mocker.patch("projet.components.sidebar.st")
    mock_st.sidebar.__enter__.return_value = mock_st.sidebar

    # 1. On définit des stations existantes
    s1 = mocker.Mock(id="s1", name="Station 1")
    s2 = mocker.Mock(id="s2", name="Station 2")
    mock_navigator.get_all_stations.return_value = [s1, s2]
    
    # 2. On simule un ID en session qui n'existe PAS dans la liste [s1, s2]
    # Cela va forcer .index() à lever une ValueError
    mock_st.session_state.get.return_value = "ID_INEXISTANT"
    
    # Mock pour éviter les erreurs sur le reste du rendu
    mock_st.selectbox.return_value = "s1"
    mock_st.button.return_value = False

    sidebar = Sidebar(mock_parquet_handler, mock_data_fetcher, mock_api_queue)
    sidebar.render(mock_navigator)

    # 3. Vérifications : 
    # Le code doit avoir exécuté le bloc 'except' et s'être replié sur le premier ID (s1)
    assert mock_st.session_state.selected_station_id == "s1"
