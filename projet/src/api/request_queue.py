import queue
import threading
import logging

logger = logging.getLogger(__name__)


class ApiRequestQueue:
    def __init__(self):
        self._tasks = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread = None

    def add_task(self, task, *args, **kwargs):
        self._tasks.put((task, args, kwargs))

    def _worker(self):
        while self._stop_event.is_set() is False:
            task, args, kwargs = self._tasks.get(timeout=1)
            try:
                logger.info(f"Executing task '{task.__name__}'...")
                task(*args, **kwargs)
                self._tasks.task_done()
                logger.info(f"Task '{task.__name__}' finished.")
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error executing task: {e}", exc_info=True)
        logger.info("API request worker stopped.")

    def start(self):
        if self._worker_thread is None and not self._worker_thread.is_alive():
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
