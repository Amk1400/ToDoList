from typing import List
from app.core.config import AppConfig
from app.models.models import Detail, Project
from app.services.base_service import BaseManager
from app.services.task_service import TaskManager
from app.exceptions.entity import (
    AlreadyExistsError,
    LimitExceededError,
    NotFoundError,
    ValidationError,
)


class ProjectManager(BaseManager[Project]):
    """Manager for handling all project-level operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize project manager.

        Args:
            config (AppConfig): Configuration defining validation limits.
        """
        super().__init__(config)
        self._projects: List[Project] = []
        self._task_manager: TaskManager = TaskManager(config)

    def get_all_projects(self) -> List[Project]:
        """Return all projects.

        Returns:
            List[Project]: List of existing projects.
        """
        return self._projects

    def create_project(self, detail: Detail) -> None:
        """Create a new project.

        Args:
            detail (Detail): Project title and description.

        Raises:
            AlreadyExistsError: If project title already exists.
            LimitExceededError: If project count exceeds limit.
            ValidationError: If detail validation fails.
        """
        if any(p.detail.title == detail.title for p in self._projects):
            raise AlreadyExistsError(Project(detail))
        if len(self._projects) >= self._config.max_projects:
            raise LimitExceededError(Project(detail))
        try:
            self.create(self._projects, detail, self._config.max_projects)
        except ValidationError as error:
            raise ValidationError(Project(detail)) from error

    def get_project(self, index: int) -> Project:
        """Retrieve project by index.

        Args:
            index (int): Project index.

        Returns:
            Project: Project at specified index.

        Raises:
            NotFoundError: If index is invalid.
        """
        if not (0 <= index < len(self._projects)):
            raise NotFoundError(Project(Detail("", "")))
        return self._projects[index]

    def remove_project(self, index: int) -> None:
        """Remove project.

        Args:
            index (int): Project index.

        Raises:
            NotFoundError: If index is invalid.
        """
        try:
            self.remove_entity(self._projects, index)
        except IndexError as error:
            raise NotFoundError(Project(Detail("", ""))) from error

    def update_project(self, index: int, detail: Detail) -> None:
        """Update project detail.

        Args:
            index (int): Project index.
            detail (Detail): New detail values.

        Raises:
            NotFoundError: If index is invalid.
            ValidationError: If validation fails.
        """
        try:
            self.update_entity(self._projects, index, detail)
        except IndexError as error:
            raise NotFoundError(Project(detail)) from error
        except ValueError as error:
            raise ValidationError(Project(detail)) from error

    def get_task_manager(self) -> TaskManager:
        """Return internal task manager.

        Returns:
            TaskManager: Task manager instance.
        """
        return self._task_manager

    def _entity_name(self) -> str:
        """Return entity name.

        Returns:
            str: 'Project'.
        """
        return "Project"

    def _create_entity(self, detail: Detail) -> Project:
        """Create project instance.

        Args:
            detail (Detail): Project data.

        Returns:
            Project: New project instance.
        """
        return Project(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate project detail.

        Args:
            detail (Detail): Data to validate.

        Raises:
            ValidationError: If validation fails.
        """
        max_name = self._config.max_project_name_length
        max_desc = self._config.max_project_description_length
        try:
            self._validate_detail(detail, max_name, max_desc, "Project")
        except ValueError as error:
            raise ValidationError(Project(detail)) from error

    def _update_entity_detail(self, entity: Project, detail: Detail) -> None:
        """Apply updated detail.

        Args:
            entity (Project): Target project.
            detail (Detail): New detail.
        """
        entity.detail = detail
