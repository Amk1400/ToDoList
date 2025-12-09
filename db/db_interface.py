from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Optional

from models.models import Project, Task

T = TypeVar("T", Project, Task)


class DatabaseInterface(ABC, Generic[T]):

    def __init__(self):
        self._projects: List[Project] = []

    @abstractmethod
    def add_project(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_project(self, project: Project) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_task(self, project: Project, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_task(self, project: Project, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_entity(self, old_entity: T, new_entity: T, parent_project: Optional[Project]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_projects(self) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    def get_tasks(self, project: Project) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    def _load(self) -> None:
        raise NotImplementedError