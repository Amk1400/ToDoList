from typing import List
from dataclasses import dataclass


@dataclass
class Project:
    """Represents a project entity."""
    name: str
    description: str


class ProjectManager:
    """Handles project data operations with validation."""

    def __init__(self, max_projects: int) -> None:
        self._projects: List[Project] = []
        self._max_projects: int = max_projects

    def get_all_projects(self) -> List[Project]:
        """Return all stored projects."""
        return self._projects

    def create_project(self, name: str, description: str) -> None:
        """Create a new project entry."""
        self._validate_new_project(name, description)
        project = Project(name=name.strip(), description=description.strip())
        self._projects.append(project)

    def update_project_name(self, index: int, new_name: str) -> None:
        """Update a project name by index."""
        try:
            name = new_name.strip()
            if not name:
                raise ValueError("New project name cannot be empty.")
            if len(name) < 30:
                raise ValueError("Project name must be at least 30 characters long.")
            if any(p.name == name for p in self._projects):
                raise ValueError("Project name must be unique.")
            self._projects[index].name = name
        except IndexError as e:
            raise IndexError("Invalid project index.") from e

    def remove_project(self, index: int) -> None:
        """Remove project by index."""
        try:
            del self._projects[index]
        except IndexError as e:
            raise IndexError("Invalid project index.") from e

    def _validate_new_project(self, name: str, description: str) -> None:
        """Validate project before creation."""
        if len(name.strip()) >= 30:
            raise ValueError("Project name must be at last 30 characters long.")
        if len(description.strip()) >= 150:
            raise ValueError("Project description must be at last 150 characters long.")
        if any(p.name == name.strip() for p in self._projects):
            raise ValueError("Project name must be unique.")
        if len(self._projects) >= self._max_projects:
            raise OverflowError("Maximum number of projects reached.")
