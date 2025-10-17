from typing import List
from config import AppConfig
from models import Detail, Project
from managers.base_manager import BaseManager
from managers.task_manager import TaskManager


class ProjectManager(BaseManager[Project]):
    """Manages all projects and delegates task operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize project manager."""
        super().__init__(config)
        self._projects: List[Project] = []
        self._task_manager: TaskManager = TaskManager(config)

    def get_all_projects(self) -> List[Project]:
        """Return all projects."""
        return self._projects

    def create_project(self, detail: Detail) -> None:
        """Create a new project."""
        if any(p.detail.title == detail.title for p in self._projects):
            raise ValueError("Project title must be unique.")
        self.create(self._projects, detail, self._config.max_projects)

    def get_project(self, index: int) -> Project:
        """Return a project by index."""
        return self.get_entity(self._projects, index)

    def remove_project(self, index: int) -> None:
        """Remove a project."""
        self.remove_entity(self._projects, index)

    def update_project(self, index: int, detail: Detail) -> None:
        """Update project details."""
        self.update_entity(self._projects, index, detail)

    def get_task_manager(self) -> TaskManager:
        """Return the task manager instance."""
        return self._task_manager

    def _entity_name(self) -> str:
        """Return entity name."""
        return "Project"

    def _create_entity(self, detail: Detail) -> Project:
        """Factory for creating a project."""
        return Project(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate project detail fields."""
        max_name = self._config.max_project_name_length
        max_description = self._config.max_project_description_length
        self._validate_detail(detail, max_name, max_description,"Project")

    def _update_entity_detail(self, entity: Project, detail: Detail) -> None:
        """Apply updated detail to a project."""
        entity.detail = detail