from typing import List


class ProjectManager:
    """Handles internal project data operations."""

    def __init__(self) -> None:
        self._projects: List[str] = []

    def get_all_projects(self) -> List[str]:
        """Return all stored projects."""
        return self._projects

    def create_project(self, name: str) -> None:
        """Create a new project entry."""
        if not name.strip():
            raise ValueError("Project name cannot be empty.")
        self._projects.append(name.strip())

    def update_project_name(self, index: int, new_name: str) -> None:
        """Update a project name by index."""
        try:
            if not new_name.strip():
                raise ValueError("New project name cannot be empty.")
            self._projects[index] = new_name.strip()
        except IndexError as e:
            raise IndexError("Invalid project index.") from e

    def remove_project(self, index: int) -> None:
        """Remove project by index."""
        try:
            del self._projects[index]
        except IndexError as e:
            raise IndexError("Invalid project index.") from e
