from dataclasses import dataclass, field
from datetime import date
from typing import List, Callable


@dataclass
class Detail:
    """Entity metadata container."""
    title: str
    description: str


@dataclass
class Task:
    """Project task item."""
    detail: Detail
    deadline: date
    status: str = "todo"


@dataclass
class Project:
    """Project containing tasks."""
    detail: Detail
    tasks: List[Task] = field(default_factory=list)


@dataclass
class Option:
    """Menu option item."""
    title: str
    action: Callable[[], None]
