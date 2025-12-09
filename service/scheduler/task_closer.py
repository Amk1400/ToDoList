from datetime import datetime
from typing import List
from repository.project_repository import ProjectRepository
from repository.task_repository import TaskRepository
from models.models import Project, Task, Status


class TaskCloser:
    """Closes overdue tasks by directly interacting with repositories."""

    def __init__(self, project_repo: ProjectRepository, task_repo: TaskRepository):
        self._project_repo = project_repo
        self._task_repo = task_repo

    def close_overdue_tasks(self) -> None:
        """Mark all overdue tasks as done and set closed_at."""
        now = datetime.now()
        projects: List[Project] = self._project_repo.get_db_list()

        for project in projects:
            tasks: List[Task] = self._task_repo.get_db_list(project)
            for task in tasks:
                if task.deadline < now and getattr(task, "status", "") != "done":
                    old_task = task
                    new_task = Task(
                        detail=task.detail,
                        deadline=task.deadline,
                        status=Status.DONE,
                        closed_at = now
                    )
                    setattr(new_task, "closed_at", datetime.now())
                    self._task_repo.update_entity(project, old_task, new_task)
