import pytest
from projet.src.data_structures.linked_list_node import StationNode
from projet.src.data_structures.linked_list_navigator import LinkedListNavigator

@pytest.fixture
def mock_station(mocker):
    return mocker.Mock(name="Station1")

@pytest.fixture
def stations(mocker):
    s1 = mocker.Mock(name="Station1")
    s2 = mocker.Mock(name="Station2")
    s3 = mocker.Mock(name="Station3")
    return [s1, s2, s3]

# =============================================================================
# TESTS StationNode
# =============================================================================

def test_node_creation(mock_station):
    """Test : Création d'un noeud simple"""
    node = StationNode(station=mock_station)
    assert node.station == mock_station
    assert node.next is None
    assert node.previous is None

# =============================================================================
# TESTS LinkedListNavigator
# =============================================================================

def test_navigator_empty():
    """Test : Navigator avec liste vide"""
    nav = LinkedListNavigator([])
    assert nav.get_current() is None
    assert nav.get_all_stations() == []
    
    # Navigation sur vide
    assert nav.get_next() is None
    assert nav.get_previous() is None
    
    with pytest.raises(ValueError):
        nav.set_current("Anything")

def test_navigator_initialization(stations):
    """Test : Initialisation correcte et liens circulaires"""
    nav = LinkedListNavigator(stations)
    
    # Vérifie start = premier élément
    assert nav.get_current() == stations[0]
    
    # Vérifie liste complète
    assert nav.get_all_stations() == stations

def test_navigator_navigation_next(stations):
    """Test : Navigation vers le suivant (circulaire)"""
    nav = LinkedListNavigator(stations)
    
    # 0 -> 1
    assert nav.get_next() == stations[1]
    # 1 -> 2
    assert nav.get_next() == stations[2]
    # 2 -> 0 (boucle)
    assert nav.get_next() == stations[0]

def test_navigator_navigation_previous(stations):
    """Test : Navigation vers le précédent (circulaire)"""
    nav = LinkedListNavigator(stations)
    
    # 0 -> 2 (boucle arrière)
    assert nav.get_previous() == stations[2]
    # 2 -> 1
    assert nav.get_previous() == stations[1]
    # 1 -> 0
    assert nav.get_previous() == stations[0]

def test_navigator_set_current(stations):
    """Test : Définir la station courante manuellement"""
    nav = LinkedListNavigator(stations)
    
    # Changement vers station 2
    nav.set_current(stations[1])
    assert nav.get_current() == stations[1]
    
    # Vérifie que la navigation continue depuis là
    assert nav.get_next() == stations[2]

def test_navigator_set_current_invalid(stations, mocker):
    """Test : Erreur si station inconnue"""
    nav = LinkedListNavigator(stations)
    unknown = mocker.Mock(name="Unknown")
    
    with pytest.raises(ValueError):
        nav.set_current(unknown)

def test_navigator_single_element(mock_station):
    """Test : Cas particulier d'une liste à 1 élément (boucle sur lui-même)"""
    nav = LinkedListNavigator([mock_station])
    
    assert nav.get_current() == mock_station
    assert nav.get_next() == mock_station
    assert nav.get_previous() == mock_station
