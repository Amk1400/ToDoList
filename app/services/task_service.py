from typing import Optional
from app.models.models import Task, Detail, Status, Project
from app.services.entity_service import EntityManager
from app.core.config import AppConfig


class TaskManager(EntityManager[Task]):
    """Manager for task domain rules."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize task manager."""
        super().__init__(config)
        self._config = config

    def _get_limit_count(self) -> int:
        """Return max tasks allowed."""
        return self._config.max_tasks

    def _get_limits(self) -> tuple[int, int]:
        """Return max title and description length for tasks."""
        return self._config.max_task_name_length, self._config.max_task_description_length

    def list_tasks_for_project(self, project: Project) -> list[Task]:
        """Return tasks belonging to a project."""
        return list(project.tasks)

    def create_task_for_project(self, project: Project, task: Task, detail: Detail) -> Task:
        """Create task inside a project."""
        task = self.create_entity(task, detail)
        project.tasks.append(task)
        return task

    def update_task_for_project(self, project: Project, index: int, detail: Detail, status: Optional[Status] = None) -> Task:
        """Update task inside a project."""
        task = self.update_entity(index, detail, status)
        project.tasks[index] = task
        return task

    def remove_task_from_project(self, project: Project, index: int) -> None:
        """Remove task from project."""
        self.remove_entity(index)
        del project.tasks[index]