from typing import List
from core.config import AppConfig
from models import Detail, Project
from service.base_manager import BaseManager
from service.task_manager import TaskManager


class ProjectManager(BaseManager[Project]):
    """Manager class responsible for handling all project-level operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize the project manager.

        Args:
            config (AppConfig): Configuration object defining validation limits.
        """
        super().__init__(config)
        self._projects: List[Project] = []
        self._task_manager: TaskManager = TaskManager(config)

    def get_all_projects(self) -> List[Project]:
        """Return all projects in memory.

        Returns:
            List[Project]: A list of all existing projects.
        """
        return self._projects

    def create_project(self, detail: Detail) -> None:
        """Create a new project with validation.

        Args:
            detail (Detail): The project's title and description.

        Raises:
            ValueError: If a project with the same title already exists.
            OverflowError: If the maximum number of projects is reached.
        """
        if any(p.detail.title == detail.title for p in self._projects):
            raise ValueError("Project title must be unique.")
        self.create(self._projects, detail, self._config.max_projects)

    def get_project(self, index: int) -> Project:
        """Retrieve a project by its index.

        Args:
            index (int): Index of the project to retrieve.

        Returns:
            Project: The project at the specified index.

        Raises:
            IndexError: If the index is invalid.
        """
        return self.get_entity(self._projects, index)

    def remove_project(self, index: int) -> None:
        """Remove a project from the system.

        Args:
            index (int): Index of the project to remove.

        Raises:
            IndexError: If the index is invalid.
        """
        self.remove_entity(self._projects, index)

    def update_project(self, index: int, detail: Detail) -> None:
        """Update the detail of a project.

        Args:
            index (int): Index of the project to update.
            detail (Detail): The new title and description for the project.

        Raises:
            IndexError: If the index is invalid.
            ValueError: If validation of project detail fails.
        """
        self.update_entity(self._projects, index, detail)

    def get_task_manager(self) -> TaskManager:
        """Return the internal task manager instance.

        Returns:
            TaskManager: The task manager associated with this project manager.
        """
        return self._task_manager

    def _entity_name(self) -> str:
        """Return the entity name for identification.

        Returns:
            str: The string 'Project'.
        """
        return "Project"

    def _create_entity(self, detail: Detail) -> Project:
        """Factory method to create a new project instance.

        Args:
            detail (Detail): Project title and description.

        Returns:
            Project: A new project instance.
        """
        return Project(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate project detail fields against configuration limits.

        Args:
            detail (Detail): The detail object to validate.

        Raises:
            ValueError: If validation fails for title or description.
        """
        max_name = self._config.max_project_name_length
        max_description = self._config.max_project_description_length
        self._validate_detail(detail, max_name, max_description, "Project")

    def _update_entity_detail(self, entity: Project, detail: Detail) -> None:
        """Apply updated detail to a project entity.

        Args:
            entity (Project): The project to update.
            detail (Detail): The new detail data.
        """
        entity.detail = detail
