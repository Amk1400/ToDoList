from dataclasses import dataclass, field
from datetime import date
from typing import List, Callable


@dataclass
class Detail:
    """Entity metadata container."""
    title: str
    description: str


@dataclass
class Entity:
    """Abstract base for all entities."""
    detail: Detail


@dataclass
class Task(Entity):
    """Project task item."""
    deadline: date
    status: str = "todo"

    def __str__(self) -> str:
        return f"{self.detail.title} ({self.detail.description}) - {self.status}, {self.deadline}"


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
