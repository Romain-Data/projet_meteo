import queue
import logging
import threading
from typing import Callable, Any


logger = logging.getLogger(__name__)


class ApiRequestQueue:
    """
    Gère une file d'attente pour exécuter des tâches (comme des requêtes API)
    en arrière-plan pour ne pas bloquer l'application principale.
    """
    def __init__(self, task_status: dict | None = None):
        self._task_status = task_status
        self._tasks = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread = None
        self._is_busy = False

    @property
    def is_working(self):
        return self._is_busy or not self._tasks.empty()

    def add_task(self, task: Callable[..., Any], on_complete: Callable[[], None] = None, *args, **kwargs):
        self._tasks.put((task, args, kwargs, on_complete))

    def _worker(self):
        while not self._stop_event.is_set():
            try:
                task, args, kwargs, on_complete = self._tasks.get(timeout=1)
                self._is_busy = True
                try:
                    logger.info(f"Executing task '{task.__name__}'...")
                    task(*args, **kwargs)
                    
                    # Mise à jour directe du statut partagé (thread-safe pour les dicts)
                    if self._task_status is not None:
                        self._task_status["refresh_needed"] = True

                    if on_complete:
                        on_complete()
                    logger.info(f"Task '{task.__name__}' finished.")
                except Exception as e:
                    logger.error(f"Error executing task: {e}", exc_info=True)
                finally:
                    self._is_busy = False
                    self._tasks.task_done()

            except queue.Empty:
                continue
        logger.info("API request worker stopped.")

    def start(self):
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._stop_event.clear()
            self._worker_thread = threading.Thread(target=self._worker, daemon=True)
            self._worker_thread.start()
            logger.info("Worker thread started.")

    def stop(self):
        logger.info("Stopping worker thread...")
        self._stop_event.set()
        if self._worker_thread:
            self._worker_thread.join()
        logger.info("Worker thread stopped successfully.")
