from typing import List
from app.core.config import AppConfig
from app.models.models import Detail, Task, Project
from app.services.base_service import BaseManager
from app.exceptions.entity import (
    AlreadyExistsError,
    LimitExceededError,
    NotFoundError,
    ValidationError,
    StatusError,
)


class TaskManager(BaseManager[Task]):
    """Manager for handling all task-level operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize task manager.

        Args:
            config (AppConfig): Configuration defining validation limits.
        """
        super().__init__(config)
        self._tasks: List[Task] = []

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks.

        Returns:
            List[Task]: List of existing tasks.
        """
        return self._tasks

    def create_task(self, detail: Detail) -> None:
        """Create a new task.

        Args:
            detail (Detail): Task title and description.

        Raises:
            AlreadyExistsError: If task title already exists.
            LimitExceededError: If task count exceeds limit.
            ValidationError: If validation fails.
        """
        if any(t.detail.title == detail.title for t in self._tasks):
            raise AlreadyExistsError(Task(detail))
        if len(self._tasks) >= self._config.max_tasks:
            raise LimitExceededError(Task(detail))
        try:
            self.create(self._tasks, detail, self._config.max_tasks)
        except ValidationError as error:
            raise ValidationError(Task(detail)) from error

    def get_task(self, index: int) -> Task:
        """Retrieve task by index.

        Args:
            index (int): Task index.

        Returns:
            Task: Task at specified index.

        Raises:
            NotFoundError: If index is invalid.
        """
        if not (0 <= index < len(self._tasks)):
            raise NotFoundError(Task(Detail("", "")))
        return self._tasks[index]

    def remove_task(self, index: int) -> None:
        """Remove task.

        Args:
            index (int): Task index.

        Raises:
            NotFoundError: If index is invalid.
        """
        try:
            self.remove_entity(self._tasks, index)
        except IndexError as error:
            raise NotFoundError(Task(Detail("", ""))) from error

    def update_task(self, index: int, detail: Detail) -> None:
        """Update task detail.

        Args:
            index (int): Task index.
            detail (Detail): New detail values.

        Raises:
            NotFoundError: If index is invalid.
            ValidationError: If validation fails.
        """
        try:
            self.update_entity(self._tasks, index, detail)
        except IndexError as error:
            raise NotFoundError(Task(detail)) from error
        except ValueError as error:
            raise ValidationError(Task(detail)) from error

    def toggle_task_status(self, index: int) -> None:
        """Toggle completion status of a task.

        Args:
            index (int): Task index.

        Raises:
            NotFoundError: If index is invalid.
            StatusError: If task status update fails.
        """
        try:
            task = self.get_task(index)
            task.is_completed = not task.is_completed
        except NotFoundError as error:
            raise NotFoundError(Task(Detail("", ""))) from error
        except Exception as error:
            raise StatusError(Task(Detail("", ""))) from error

    def _entity_name(self) -> str:
        """Return entity name.

        Returns:
            str: 'Task'.
        """
        return "Task"

    def _create_entity(self, detail: Detail) -> Task:
        """Create task instance.

        Args:
            detail (Detail): Task data.

        Returns:
            Task: New task instance.
        """
        return Task(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate task detail.

        Args:
            detail (Detail): Data to validate.

        Raises:
            ValidationError: If validation fails.
        """
        max_name = self._config.max_task_name_length
        max_desc = self._config.max_task_description_length
        try:
            self._validate_detail(detail, max_name, max_desc, "Task")
        except ValueError as error:
            raise ValidationError(Task(detail)) from error

    def _update_entity_detail(self, entity: Task, detail: Detail) -> None:
        """Apply updated detail.

        Args:
            entity (Task): Target task.
            detail (Detail): New detail.
        """
        entity.detail = detail
