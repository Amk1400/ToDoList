from schedule import every, run_pending
import time
from typing import List
from threading import Thread

from service.scheduler.task_closer import TaskCloser


class TaskScheduler:
    """Runs scheduled background task closures."""
    """
    Attributes:
        _jobs (List[TaskCloser]): List of task closers.
        _stop (bool): Flag to stop loop.
    """

    def __init__(self, jobs: List[TaskCloser]) -> None:
        """Initialize scheduler with job list."""
        """
        Args:
            jobs (List[TaskCloser]): Tasks to schedule.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._jobs = jobs
        self._stop = False

    def start_background(self) -> None:
        """Start periodic scheduler in background thread."""
        """
        Args:
            None

        Returns:
            None: No return value.

        Raises:
            Exception: If scheduling setup fails.
        """
        for job in self._jobs:
            every().day.at("21:55").do(job.close_overdue_tasks)

        thread = Thread(target=self._run_loop, daemon=True)
        thread.start()

    def _run_loop(self) -> None:
        """Run loop executing pending jobs."""
        """
        Args:
            None

        Returns:
            None: No return value.

        Raises:
            None
        """
        while not self._stop:
            run_pending()
            time.sleep(1)

    def stop(self) -> None:
        """Stop scheduler loop."""
        """
        Args:
            None

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._stop = True
