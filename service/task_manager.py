from datetime import date
from typing import Optional, List

from core.config import AppConfig
from models.models import Detail, Task, Project, Status
from repository.task_repository import TaskRepository
from service.entity_manager import EntityManager
from service.validators import Validators


class TaskManager(EntityManager[Task]):
    """Manager for task-level operations."""
    """
    Attributes:
        _parent_project (Optional[Project]): Current parent project.
    """

    def __init__(
        self,
        config: AppConfig,
        db,
        current_project: Optional[Project] = None,
    ) -> None:
        """Initialize task manager with repository and project."""
        """
        Args:
            config (AppConfig): App configuration.
            db: Database session or handler.
            current_project (Optional[Project]): Initial project.

        Returns:
            None: No return value.

        Raises:
            Exception: If initialization fails.
        """
        repository = TaskRepository(db)
        super().__init__(config, repository)
        self._parent_project: Optional[Project] = None
        if current_project:
            self.set_parent_project(current_project)

    def set_parent_project(self, project: Project) -> None:
        """Assign parent project."""
        """
        Args:
            project (Project): Target project.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._parent_project = project

    def entity_name(self) -> str:
        """Return entity name."""
        """
        Args:
            None

        Returns:
            str: Name of entity.

        Raises:
            None
        """
        return "Task"

    def create_entity_object(
        self,
        detail: Detail,
        deadline: Optional[date] = None,
        status: Optional[Status] = Status.TODO,
    ) -> Task:
        """Create task entity."""
        """
        Args:
            detail (Detail): Detail metadata.
            deadline (Optional[date]): Task deadline.
            status (Optional[Status]): Task status.

        Returns:
            Task: Constructed task.

        Raises:
            None
        """
        return Task(detail=detail, deadline=deadline, status=status)

    def _update_deadline_and_status_by_repo(
        self,
        deadline: Optional[date],
        entity: Task,
        status: Optional[str],
    ) -> None:
        """Update task deadline and status."""
        """
        Args:
            deadline (Optional[date]): New deadline.
            entity (Task): Target entity.
            status (Optional[str]): New status.

        Returns:
            None: No return value.

        Raises:
            ValueError: If status validation fails.
        """
        if deadline is not None:
            entity.deadline = deadline
        if status is not None:
            entity.status = Validators.validate_status(status)

    def _get_max_desc_length(self) -> int:
        """Return max description length."""
        """
        Args:
            None

        Returns:
            int: Max allowed length.

        Raises:
            None
        """
        return self._config.max_task_description_length

    def _get_max_title_length(self) -> int:
        """Return max title length."""
        """
        Args:
            None

        Returns:
            int: Max title length.

        Raises:
            None
        """
        return self._config.max_task_name_length

    def _get_max_count(self) -> int:
        """Return max task count."""
        """
        Args:
            None

        Returns:
            int: Maximum number.

        Raises:
            None
        """
        return self._config.max_tasks

    def remove_entity_object(self, entity: Task) -> None:
        """Remove task entity."""
        """
        Args:
            entity (Task): Target entity.

        Returns:
            None: No return value.

        Raises:
            ValueError: If parent project missing.
        """
        self._remove_from_repository(entity, self._parent_project)

    def get_repo_list(self) -> List[Task]:
        """Retrieve repository items for current project."""
        """
        Args:
            None

        Returns:
            List[Task]: Task list.

        Raises:
            ValueError: If parent project not set.
        """
        if self._parent_project is None:
            raise ValueError("Current project is not set for TaskManager.")
        return self._repository.get_db_list(self._parent_project)

    def _append_to_repository(self, entity: Task) -> None:
        """Append task entity to repository."""
        """
        Args:
            entity (Task): Task to append.

        Returns:
            None: No return value.

        Raises:
            ValueError: If parent project missing.
        """
        if self._parent_project is None:
            raise ValueError("Current project is not set for TaskManager.")
        self._repository.append_to_db(entity, self._parent_project)

    def _remove_from_repository(
        self,
        entity: Task,
        parent_project: Optional[Project] = None,
    ) -> None:
        """Remove task from project repository."""
        """
        Args:
            entity (Task): Task entity.
            parent_project (Optional[Project]): Parent project.

        Returns:
            None: No return value.

        Raises:
            ValueError: If parent project missing.
        """
        if parent_project is None:
            raise ValueError("Parent project must be provided for tasks.")
        self._repository.remove_from_db(entity, parent_project)

    def get_parent_project(self) -> Project:
        """Return parent project."""
        """
        Args:
            None

        Returns:
            Project: Current parent project.

        Raises:
            None
        """
        return self._parent_project
