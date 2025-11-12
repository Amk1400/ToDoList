from typing import List
from app.core.config import AppConfig
from app.models.models import Detail, Task, Project
from app.services.entity_service import EntityManager
from app.exceptions.entity import ValidationError, StatusError, NotFoundError


class TaskManager(EntityManager[Task]):
    """Manages all task-related operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize task manager.

        Args:
            config (AppConfig): Configuration for task limits.
        """
        super().__init__(config)
        self._tasks: List[Task] = []

    def _entity_type(self) -> type:
        """Return entity type."""
        return Task

    def get_collection(self, parent: Project | None = None) -> List[Task]:
        """Return tasks of a project."""
        return parent.tasks if parent else self._tasks

    def _get_limit(self, parent: Project | None = None) -> int:
        """Return task limit."""
        return self._config.max_tasks

    def _create_entity(self, detail: Detail) -> Task:
        """Create task entity."""
        return Task(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate task detail."""
        try:
            self._validate_detail(
                detail,
                self._config.max_task_name_length,
                self._config.max_task_description_length,
            )
        except Exception as error:
            raise ValidationError("Task") from error

    def _update_entity_detail(self, entity: Task, detail: Detail) -> None:
        """Apply new task detail."""
        entity.detail = detail

    def toggle_task_status(self, index: int) -> None:
        """Toggle completion status.

        Args:
            index (int): Task index.

        Raises:
            NotFoundError: If index invalid.
            StatusError: If toggle fails.
        """
        try:
            task = self.get_entity(self._tasks, index)
            task.is_completed = not task.is_completed
        except NotFoundError as error:
            raise NotFoundError("Task") from error
        except Exception as error:
            raise StatusError("Task") from error

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks."""
        return self._tasks