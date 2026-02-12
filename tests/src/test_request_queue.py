import pytest
import threading
from queue import Empty
from projet.src.api.request_queue import ApiRequestQueue

@pytest.fixture
def queue_instance():
    return ApiRequestQueue()

def test_add_task(queue_instance, mocker):
    """Test : Ajout d'une tâche dans la queue"""
    func = mocker.Mock()
    queue_instance.add_task(func, "arg1", key="val1")
    
    assert not queue_instance._tasks.empty()
    item = queue_instance._tasks.get()
    
    # Structure de l'item: (task, args, kwargs, on_complete)
    assert item[0] == func
    assert item[1] == ("arg1",)
    assert item[2] == {"key": "val1"}
    assert item[3] is None

def test_start_creates_thread(queue_instance, mocker):
    """Test : start() lance bien un thread"""
    mock_thread = mocker.patch("threading.Thread")
    mock_thread_instance = mock_thread.return_value
    
    queue_instance.start()
    
    mock_thread.assert_called_once()
    mock_thread_instance.start.assert_called_once()
    assert queue_instance._worker_thread is not None

def test_stop_sets_event(queue_instance, mocker):
    """Test : stop() arrête le thread"""
    mock_thread = mocker.Mock()
    queue_instance._worker_thread = mock_thread
    mock_thread.is_alive.return_value = True
    
    queue_instance.stop()
    
    assert queue_instance._stop_event.is_set()
    mock_thread.join.assert_called_once()

def test_worker_executes_task(queue_instance, mocker):
    """Test : _worker exécute la tâche et update le status"""
    task = mocker.Mock(name="Task")
    task.__name__ = "MockTask"  # Required for logger.info(task.__name__)
    on_complete = mocker.Mock(name="Callback")
    status = {}
    queue_instance._task_status = status
    
    # On ajoute une tâche
    queue_instance.add_task(task, "test", on_complete=on_complete)
    
    # On ruse pour ne faire qu'un tour de boucle
    # is_set() est appelé au début du while. 
    # 1er appel: False (entre dans la boucle). 2eme appel: True (sort).
    mocker.patch.object(queue_instance._stop_event, 'is_set', side_effect=[False, True])
    
    queue_instance._worker()
    
    # Vérifications
    task.assert_called_once_with("test")
    on_complete.assert_called_once()
    assert status["refresh_needed"] is True
    assert queue_instance._is_busy is False

def test_worker_handle_exception(queue_instance, mocker):
    """Test : Le worker ne plante pas si la tâche lève une exception"""
    task = mocker.Mock(side_effect=ValueError("Boom"))
    task.__name__ = "MockTask"
    
    queue_instance.add_task(task)
    
    mocker.patch.object(queue_instance._stop_event, 'is_set', side_effect=[False, True])

    queue_instance._worker()
    
    task.assert_called_once()
    assert queue_instance._is_busy is False


def test_is_working_property(queue_instance, mocker):
    """Test : Property is_working"""
    # Cas 1: Ni busy, ni task
    assert queue_instance.is_working is False
    
    # Cas 2: Busy
    queue_instance._is_busy = True
    assert queue_instance.is_working is True
    queue_instance._is_busy = False
    
    # Cas 3: Queue non vide
    queue_instance.add_task(lambda: None)
    assert queue_instance.is_working is True

def test_start_already_running(queue_instance, mocker):
    """Test : start() ne fait rien si thread déjà en cours"""
    mock_thread = mocker.Mock()
    mock_thread.is_alive.return_value = True
    queue_instance._worker_thread = mock_thread
    
    # Appel start
    queue_instance.start()
    
    # Vérifie qu'on n'a pas recréé de thread ni rappelé start
    # (Le mock_thread initial a été créé manuellement, donc start n'a pas été appelé dessus par nous)
    mock_thread.start.assert_not_called()

def test_stop_no_thread(queue_instance, mocker):
    """Test : stop() sans thread actif ne plante pas"""
    queue_instance._worker_thread = None
    queue_instance.stop()
    assert queue_instance._stop_event.is_set()

def test_stop_dead_thread(queue_instance, mocker):
    """Test : stop() avec thread mort ne plante pas"""
    mock_thread = mocker.Mock()
    queue_instance._worker_thread = mock_thread
    
    queue_instance.stop()
    
    assert queue_instance._stop_event.is_set()
    mock_thread.join.assert_called_once()

def test_worker_success_no_status_no_callback(queue_instance, mocker):
    """Test : Exécution réussie sans task_status ni on_complete"""
    task = mocker.Mock(name="Task")
    task.__name__ = "MsTask"
    
    # Ensure queue has no status
    queue_instance._task_status = None
    
    # Add task without callback
    queue_instance.add_task(task)
    
    mocker.patch.object(queue_instance._stop_event, 'is_set', side_effect=[False, True])
    
    queue_instance._worker()
    

def test_worker_timeout(queue_instance, mocker):
    """Test : Worker gère le timeout de la queue (queue.Empty)"""
    # On mock queue.get pour qu'il lève Empty
    # 1er appel à stop_event.is_set -> False (rentre dans la boucle)
    # 2eme appel -> True (sort de la boucle)
    mocker.patch.object(queue_instance._stop_event, 'is_set', side_effect=[False, True])
    
    # On mock _tasks.get pour lever Empty
    mocker.patch.object(queue_instance._tasks, 'get', side_effect=Empty)
    
    queue_instance._worker()
    
    # Vérifie que get a été appelé
    queue_instance._tasks.get.assert_called_once()
