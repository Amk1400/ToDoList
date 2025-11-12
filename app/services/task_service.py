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
    """Handles all task-level operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize task manager.

        Args:
            config (AppConfig): Configuration limits for tasks.
        """
        super().__init__(config)
        self._tasks: List[Task] = []

    def create_task_for_project(self, project: Project, detail: Detail) -> None:
        """Create and attach a task to a project.

        Args:
            project (Project): Project to attach the new task.
            detail (Detail): Task title and description.

        Raises:
            AlreadyExistsError: If task title already exists.
            LimitExceededError: If task count exceeds limits.
            ValidationError: If detail validation fails.
        """
        if any(t.detail.title == detail.title for t in project.tasks):
            raise AlreadyExistsError(Task(detail))
        if len(project.tasks) >= self._config.max_tasks:
            raise LimitExceededError(Task(detail))

        try:
            new_task = self._create_entity(detail)
            self._validate(detail)
            project.tasks.append(new_task)
            self._tasks.append(new_task)
        except ValidationError as error:
            raise ValidationError(Task(detail)) from error

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks.

        Returns:
            List[Task]: List of existing tasks.
        """
        return self._tasks

    def get_task(self, index: int) -> Task:
        """Retrieve task by index.

        Args:
            index (int): Task index.

        Returns:
            Task: Task instance.

        Raises:
            NotFoundError: If index invalid.
        """
        if not (0 <= index < len(self._tasks)):
            raise NotFoundError(Task(Detail("", "")))
        return self._tasks[index]

    def update_task(self, index: int, detail: Detail) -> None:
        """Update task detail.

        Args:
            index (int): Task index.
            detail (Detail): New task detail.

        Raises:
            NotFoundError: If index invalid.
            ValidationError: If validation fails.
        """
        try:
            self.update_entity(self._tasks, index, detail)
        except IndexError as error:
            raise NotFoundError(Task(detail)) from error
        except ValueError as error:
            raise ValidationError(Task(detail)) from error

    def remove_task(self, index: int) -> None:
        """Remove a task.

        Args:
            index (int): Task index.

        Raises:
            NotFoundError: If index invalid.
        """
        try:
            self.remove_entity(self._tasks, index)
        except IndexError as error:
            raise NotFoundError(Task(Detail("", ""))) from error

    def toggle_task_status(self, index: int) -> None:
        """Toggle task completion status.

        Args:
            index (int): Task index.

        Raises:
            NotFoundError: If index invalid.
            StatusError: If toggle fails.
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
        """Create task entity.

        Args:
            detail (Detail): Task detail.

        Returns:
            Task: New task.
        """
        return Task(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate task detail.

        Args:
            detail (Detail): Task data.

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
