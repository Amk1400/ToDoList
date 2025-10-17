from typing import List
from dataclasses import dataclass


@dataclass
class Project:
    """Represents a project entity."""
    name: str
    description: str


class ProjectManager:
    """Handles project data operations with validation."""

    def __init__(
        self,
        max_projects: int,
        max_name_length: int,
        max_description_length: int,
    ) -> None:
        self._projects: List[Project] = []
        self._max_projects: int = max_projects
        self._max_name_length: int = max_name_length
        self._max_description_length: int = max_description_length

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
            self._validate_project_name(name)
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
        self._validate_project_name(name)
        self._validate_project_description(description)
        if any(p.name == name.strip() for p in self._projects):
            raise ValueError("Project name must be unique.")
        if len(self._projects) >= self._max_projects:
            raise OverflowError("Maximum number of projects reached.")

    def _validate_project_name(self, name: str) -> None:
        """Validate project name constraints."""
        stripped = name.strip()
        if not stripped:
            raise ValueError("Project name cannot be empty.")
        if len(stripped) < self._max_name_length:
            raise ValueError(
                f"Project name must be at least {self._max_name_length} characters long."
            )
        if len(stripped) > self._max_name_length:
            raise ValueError(
                f"Project name cannot exceed {self._max_name_length} characters."
            )

    def _validate_project_description(self, description: str) -> None:
        """Validate project description constraints."""
        stripped = description.strip()
        if not stripped:
            raise ValueError("Project description cannot be empty.")
        if len(stripped) < self._max_description_length:
            raise ValueError(
                f"Project description must be at least {self._max_description_length} characters long."
            )
        if len(stripped) > self._max_description_length:
            raise ValueError(
                f"Project description cannot exceed {self._max_description_length} characters."
            )