from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from models.models import Project, Task


class DatabaseInterface(ABC):
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
