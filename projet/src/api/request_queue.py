"""
Module for managing a queue to execute tasks (such as API requests)
in the background to avoid blocking the main application.
"""

import queue
import logging
import threading
from typing import Callable, Any


logger = logging.getLogger(__name__)


class ApiRequestQueue:
    """
    Manages a queue to execute tasks (such as API requests)
    in the background to avoid blocking the main application.
    """
    def __init__(self, task_status: dict | None = None):
        self._task_status = task_status
        self._tasks = queue.Queue()
        self._stop_event = threading.Event()
        self._worker_thread = None
        self._is_busy = False

    @property
    def is_working(self):
        """
        Check if the queue is working.

        Returns:
            bool: True if the queue is working, False otherwise
        """
        return self._is_busy or not self._tasks.empty()

    def add_task(
        self,
        task: Callable[..., Any],
        *args,
        on_complete: Callable[[], None] = None,
        **kwargs
    ):
        """
        Add a task to the queue.

        Args:
            task: Task to add
            on_complete: Callback to execute after task completion
            *args: Arguments to pass to the task
            **kwargs: Keyword arguments to pass to the task
        """
        self._tasks.put((task, args, kwargs, on_complete))

    def _worker(self):
        """
        Worker thread that executes tasks from the queue.
        """
        while not self._stop_event.is_set():
            try:
                task, args, kwargs, on_complete = self._tasks.get(timeout=1)
                self._is_busy = True
                try:
                    logger.info("Executing task '%s'...", task.__name__)
                    task(*args, **kwargs)

                    # Direct update of shared status (thread-safe for dicts)
                    if self._task_status is not None:
                        self._task_status["refresh_needed"] = True

                    if on_complete:
                        on_complete()
                    logger.info("Task '%s' finished.", task.__name__)
                except Exception as e:  # pylint: disable=broad-except
                    logger.error("Error executing task: %s", e, exc_info=True)
                finally:
                    self._is_busy = False
                    self._tasks.task_done()

            except queue.Empty:
                continue
        logger.info("API request worker stopped.")

    def start(self):
        """
        Start the worker thread.
        """
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._stop_event.clear()
            self._worker_thread = threading.Thread(target=self._worker, daemon=True)
            self._worker_thread.start()
            logger.info("Worker thread started.")

    def stop(self):
        """
        Stop the worker thread.
        """
        logger.info("Stopping worker thread...")
        self._stop_event.set()
        if self._worker_thread:
            self._worker_thread.join()
        logger.info("Worker thread stopped successfully.")
