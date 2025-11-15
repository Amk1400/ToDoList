from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Detail:
    """Represents an entity's metadata containing a title and description.

    Attributes:
        title (str): The name or title of the entity.
        description (str): A short descriptive text about the entity.
    """
    title: str
    description: str


@dataclass
class Task:
    """Represents a single task within a project.

    Attributes:
        detail (Detail): The task's metadata containing title and description.
        deadline (date):
        status (str): The current task status; defaults to "todo".
            Possible values: "todo", "doing", "done".
    """
    detail: Detail
    deadline: date
    status: str = "todo"


@dataclass
class Project:
    """Represents a project that can contain multiple tasks.

    Attributes:
        detail (Detail): The project's metadata containing title and description.
        tasks (List[Task]): A list of tasks belonging to this project.
    """
    detail: Detail
    tasks: List[Task] = field(default_factory=list)

"""
#TODO new class named option
option contains a function and the name of option which is repreented in menus
"""