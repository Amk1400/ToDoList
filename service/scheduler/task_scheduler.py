from schedule import every, run_pending
import time
from typing import List
from threading import Thread

from service.scheduler.task_closer import TaskCloser


class TaskScheduler:
    """Schedules periodic task closure using schedule 1.2.2."""

    def __init__(self, jobs: List[TaskCloser]):
        self._jobs = jobs
        self._stop = False

    def start_background(self) -> None:
        """Start scheduler in background thread."""
        for job in self._jobs:
            every().day.at("21:55").do(job.close_overdue_tasks)

        thread = Thread(target=self._run_loop, daemon=True)
        thread.start()

    def _run_loop(self) -> None:
        """Run schedule loop."""
        while not self._stop:
            run_pending()
            time.sleep(1)

    def stop(self) -> None:
        """Stop background scheduler."""
        self._stop = True
