from typing import List
from config import AppConfig
from models import Project, Detail
from project_manager.task_manager import TaskManager


class ProjectManager:
    """Handles CRUD operations for projects."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize project manager."""
        self._config = config
        self._projects: List[Project] = []
        self._task_manager = TaskManager(config)

    def get_all_projects(self) -> List[Project]:
        """Return all projects."""
        return self._projects

    def create_project(self, detail: Detail) -> None:
        """Create a new project."""
        self._validate_project_details(detail)
        if len(self._projects) >= self._config.max_projects:
            raise OverflowError("Maximum number of projects reached.")
        if any(p.detail.title == detail.title for p in self._projects):
            raise ValueError("Project title must be unique.")
        self._projects.append(Project(detail=detail))

    def update_project_name(self, index: int, new_title: str) -> None:
        """Rename a project."""
        project = self._get_project(index)
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("Project title cannot be empty.")
        if any(p.detail.title == new_title for p in self._projects):
            raise ValueError("Project title must be unique.")
        if len(new_title) > self._config.max_project_name_length:
            raise ValueError(
                f"Title cannot exceed {self._config.max_project_name_length} characters."
            )
        project.detail.title = new_title

    def remove_project(self, index: int) -> None:
        """Remove a project."""
        project = self._get_project(index)
        self._projects.remove(project)

    def get_task_manager(self) -> TaskManager:
        """Provide access to the task manager."""
        return self._task_manager

    def _get_project(self, index: int) -> Project:
        """Return a project by index."""
        if not (0 <= index < len(self._projects)):
            raise IndexError("Invalid project index.")
        return self._projects[index]

    def _validate_project_details(self, detail: Detail) -> None:
        """Validate project detail fields."""
        title, description = detail.title.strip(), detail.description.strip()
        if not title:
            raise ValueError("Project title cannot be empty.")
        if len(title) > self._config.max_project_name_length:
            raise ValueError(
                f"Project title cannot exceed {self._config.max_project_name_length} characters."
            )
        if not description:
            raise ValueError("Project description cannot be empty.")
        if len(description) > self._config.max_project_description_length:
            raise ValueError(
                f"Project description cannot exceed {self._config.max_project_description_length} characters."
            )
