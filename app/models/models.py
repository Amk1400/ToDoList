from dataclasses import dataclass, field
from datetime import date
from typing import List
from enum import Enum


class Status(Enum):
    """Represents task status."""

    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Detail:
    """Basic detail information.

    Attributes:
        title (str): The title of the entity.
        description (str): The descriptive text of the entity.
    """

    title: str
    description: str

    def __str__(self) -> str:
        """Return formatted string."""
        return f"{self.title} - {self.description}"


@dataclass
class Task:
    """Task entity with detail and status.

    Attributes:
        detail (Detail): The task's detail information.
        status (Status): The current status of the task.
    """

    detail: Detail
    status: Status = Status.TODO

    def __str__(self) -> str:
        """Return formatted string."""
        return f"{self.detail.title} [{self.status.value}] - {self.detail.description}"


@dataclass
class Project:
    """Project entity containing tasks.

    Attributes:
        detail (Detail): The project's detail information.
        tasks (List[Task]): List of tasks under the project.
    """

    detail: Detail
    tasks: List[Task] = field(default_factory=list)

    def __str__(self) -> str:
        """Return formatted string."""
        return f"{self.detail.title} ({len(self.tasks)} tasks) - {self.detail.description}"
