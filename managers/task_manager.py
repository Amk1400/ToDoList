from typing import List, Optional
from config import AppConfig
from models import Detail, Task, Project
from managers.base_manager import BaseManager


class TaskManager(BaseManager[Task]):
    """Handles task-level operations for a project."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize task manager."""
        super().__init__(config)

    def add_task(self, project: Project, detail: Detail) -> None:
        """Add a new task to a project."""
        self.create(project.tasks, detail, self._config.max_tasks)

    def get_task(self, project: Project, task_index: int) -> Task:
        """Get a task by index."""
        return self.get_entity(project.tasks, task_index)

    def remove_task(self, project: Project, task_index: int) -> None:
        """Remove a task from a project."""
        self.remove_entity(project.tasks, task_index)

    def update_task(self, project: Project, task_idx: int,
                    detail: Optional[Detail] = None, status: Optional[str] = None) -> None:
        """Update task details and/or status."""
        task = self.get_entity(project.tasks, task_idx)

        if detail is not None:
            self.update_entity(project.tasks, task_idx, detail)

        if status is not None:
            if status not in {"todo", "doing", "done"}:
                raise ValueError("Invalid task status. Must be one of: todo, doing, done.")
            task.status = status

    def _entity_name(self) -> str:
        """Return entity name."""
        return "Task"

    def _create_entity(self, detail: Detail) -> Task:
        """Factory for creating a task."""
        return Task(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate task detail fields."""
        self._validate_detail(detail, self._config.max_task_name_length,
                              self._config.max_task_description_length,"Task")

    def _update_entity_detail(self, entity: Task, detail: Detail) -> None:
        """Apply updated detail to a task."""
        entity.detail = detail
