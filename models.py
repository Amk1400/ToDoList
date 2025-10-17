from dataclasses import dataclass, field
from typing import List


@dataclass
class Detail:
    """Represents title and description pair."""
    title: str
    description: str


@dataclass
class Task:
    """Represents a single task."""
    detail: Detail
    status: str = "todo"


@dataclass
class Project:
    """Represents a project containing multiple tasks."""
    detail: Detail
    tasks: List[Task] = field(default_factory=list)
