import pytest
import threading
import queue
from projet.src.api.request_queue import ApiRequestQueue

@pytest.fixture
def queue_instance():
    return ApiRequestQueue()
