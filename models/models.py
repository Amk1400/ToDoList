from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Callable, Optional


@dataclass
class Detail:
    """Metadata holder for entity fields."""

    title: str
    description: str
    """Attributes:
        title (str): Title text.
        description (str): Description text.
    """


@dataclass
class Entity:
    """Base class for all stored entities."""

    detail: Detail
    _id: int = field(default=None, init=False)

    """Attributes:
        detail (Detail): Metadata of the entity.
        _id (int): Internal identifier assigned later.
    """

    @property
    def id(self) -> int:
        """Return entity identifier.

        Returns:
            int: Stored entity ID.
        """
        return self._id


class Status(Enum):
    """Task status enumeration."""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Task(Entity):
    """Task item belonging to a project."""

    deadline: date
    status: Status = "todo"
    closed_at: Optional[date] = None

    """Attributes:
        deadline (date): Due date for the task.
        status (Status): Current progress status.
        closed_at (Optional[date]): Closing timestamp if completed.
    """

    def __str__(self) -> str:
        """Return string representation of the task.

        Returns:
            str: Formatted task information.
        """
        closed_at = (
            f" -> (closed at): {self.closed_at}"
            if self.closed_at is not None
            else ""
        )
        other = f"{self.detail.title} ({self.detail.description}) - {self.status}, {self.deadline}"
        return other + closed_at


@dataclass
class Project(Entity):
    """Project that aggregates tasks."""

    tasks: List[Task] = field(default_factory=list)

    """Attributes:
        tasks (List[Task]): Collection of project tasks.
    """

    def __str__(self) -> str:
        """Return string representation of the project.

        Returns:
            str: Formatted project information.
        """
        return f"{self.detail.title} ({self.detail.description})"


@dataclass
class Option:
    """Executable menu option."""

    title: str
    action: Callable[[], None]

    """Attributes:
        title (str): Display text of the option.
        action (Callable[[], None]): Function to execute when selected.
    """
