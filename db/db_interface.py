from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Optional
from models.models import Project, Task

T = TypeVar("T", Project, Task)


class DatabaseInterface(ABC, Generic[T]):
    """Abstract database interface for project and task operations."""

    @abstractmethod
    def add_project(self, project: Project) -> None:
        """Add a project to the database."""
        raise NotImplementedError

    @abstractmethod
    def remove_project(self, project: Project) -> None:
        """Remove a project from the database."""
        raise NotImplementedError

    @abstractmethod
    def update_entity(self, parent_project: Optional[Project], old_entity: T, new_entity: T) -> None:
        """
        Update an entity in the database.

        Args:
            parent_project (Optional[Project]): Required for tasks; None for projects.
            old_entity (T): Existing entity to update.
            new_entity (T): New entity with updated data.
        """
        raise NotImplementedError

    @abstractmethod
    def get_projects(self) -> List[Project]:
        """Return all projects from the database."""
        raise NotImplementedError

    @abstractmethod
    def add_task(self, project: Project, task: Task) -> None:
        """Add a task to a specific project."""
        raise NotImplementedError

    @abstractmethod
    def remove_task(self, project: Project, task: Task) -> None:
        """Remove a task from a specific project."""
        raise NotImplementedError

    @abstractmethod
    def get_tasks(self, project: Project) -> List[Task]:
        """Return all tasks for a specific project."""
        raise NotImplementedError
