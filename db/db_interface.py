from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Optional

from models.models import Project, Task

T = TypeVar("T", Project, Task)


class DatabaseInterface(ABC, Generic[T]):
    """Abstract interface defining database operations."""

    def __init__(self) -> None:
        """Initialize interface with internal project cache."""
        self._projects: List[Project] = []

    @abstractmethod
    def add_project(self, project: Project) -> None:
        """Add a new project.

        Args:
            project (Project): Project instance to add.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_project(self, project: Project) -> None:
        """Remove a project.

        Args:
            project (Project): Project instance to remove.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def add_task(self, project: Project, task: Task) -> None:
        """Add a task to a project.

        Args:
            project (Project): Parent project.
            task (Task): Task instance to add.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_task(self, project: Project, task: Task) -> None:
        """Remove a task from a project.

        Args:
            project (Project): Parent project.
            task (Task): Task instance to remove.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def update_entity(self, old_entity: T, new_entity: T, parent_project: Optional[Project]) -> None:
        """Update a project or task entity.

        Args:
            old_entity (T): Current entity state.
            new_entity (T): New updated entity.
            parent_project (Optional[Project]): Project context for tasks.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def get_projects(self) -> List[Project]:
        """Return all projects.

        Returns:
            List[Project]: List of existing projects.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def get_tasks(self, project: Project) -> List[Task]:
        """Return tasks of a specific project.

        Args:
            project (Project): Project to retrieve tasks from.

        Returns:
            List[Task]: Collection of project tasks.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def _load(self) -> None:
        """Load initial database state.

        Raises:
            NotImplementedError: When not implemented in subclass.
        """
        raise NotImplementedError
