import pytest
from projet.src.data_structures.linked_list_navigator import LinkedListNavigator

def test_navigator_has_next_previous_empty():
    """Test : has_next et has_previous sur liste vide"""
    nav = LinkedListNavigator([])
    
    assert nav.has_next() is False
    assert nav.has_previous() is False

def test_navigator_get_next_previous_empty():
    """Test : get_next et get_previous sur liste vide"""
    nav = LinkedListNavigator([])
    
    assert nav.get_next() is None
    assert nav.get_previous() is None

def test_navigator_has_next_previous_nominal(mocker):
    """Test : has_next et has_previous sur liste non vide"""
    station = mocker.Mock(name="Station")
    nav = LinkedListNavigator([station])
    
    assert nav.has_next() is True
    assert nav.has_previous() is True

def test_set_current_head(mocker):
    """Test : set_current sur le premier élément (head)"""
    s1 = mocker.Mock(name="S1")
    s2 = mocker.Mock(name="S2")
    nav = LinkedListNavigator([s1, s2])
    
    # On bouge à s2
    nav.set_current(s2)
    assert nav.get_current() == s2
    
    # On revient à s1 (head) via set_current
    nav.set_current(s1)
    assert nav.get_current() == s1
