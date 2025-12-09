from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Callable, Optional


@dataclass
class Detail:
    """Entity metadata container."""
    title: str
    description: str


@dataclass
class Entity:
    """Abstract base for all entities."""
    detail: Detail
    _id: int = field(default=None, init=False)

    @property
    def id(self):
        return self._id


class Status(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

@dataclass
class Task(Entity):
    """Project task item."""
    deadline: date
    status: Status= "todo"
    closed_at: Optional[date] = None

    def __str__(self) -> str:
        closed_at = f" -> (closed at): {self.closed_at}" if self.closed_at is not None else ""
        other = f"{self.detail.title} ({self.detail.description}) - {self.status}, {self.deadline}"
        return other + closed_at


@dataclass
class Project(Entity):
    """Project containing tasks."""
    tasks: List[Task] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.detail.title} ({self.detail.description})"


@dataclass
class Option:
    """Menu option item."""
    title: str
    action: Callable[[], None]
