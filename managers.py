from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a single task."""
    title: str
    description: str
    status: str = "todo"


@dataclass
class Project:
    """Represents a project containing multiple tasks."""
    name: str
    description: str
    tasks: List[Task] = field(default_factory=list)


class ProjectManager:
    """Manages all projects and their tasks."""

    def __init__(
        self,
        max_projects: int,
        max_name_length: int,
        max_description_length: int,
        max_tasks: int,
        max_task_name_length: int,
        max_task_description_length: int,
    ) -> None:
        """Initialize with dependency-injected configuration."""
        self._max_projects: int = max_projects
        self._max_name_length: int = max_name_length
        self._max_description_length: int = max_description_length
        self._max_tasks: int = max_tasks
        self._max_task_name_length: int = max_task_name_length
        self._max_task_description_length: int = max_task_description_length
        self._projects: List[Project] = []

    def get_all_projects(self) -> List[Project]:
        """Return list of all projects."""
        return self._projects

    def create_project(self, name: str, description: str) -> None:
        """Create a new project with validation."""
        if len(self._projects) >= self._max_projects:
            raise OverflowError("Maximum number of projects reached.")

        name = name.strip()
        description = description.strip()

        if not name:
            raise ValueError("Project name cannot be empty.")
        if len(name) > self._max_name_length:
            raise ValueError(f"Project name cannot exceed {self._max_name_length} characters.")
        if any(p.name == name for p in self._projects):
            raise ValueError("Project name must be unique.")
        if not description:
            raise ValueError("Project description cannot be empty.")
        if len(description) > self._max_description_length:
            raise ValueError(f"Project description cannot exceed {self._max_description_length} characters.")

        self._projects.append(Project(name=name, description=description))

    def update_project_name(self, index: int, new_name: str) -> None:
        """Update a project name by index."""
        if not (0 <= index < len(self._projects)):
            raise IndexError("Invalid project index.")

        new_name = new_name.strip()
        if not new_name:
            raise ValueError("New project name cannot be empty.")
        if len(new_name) > self._max_name_length:
            raise ValueError(f"Project name cannot exceed {self._max_name_length} characters.")
        if any(p.name == new_name for p in self._projects):
            raise ValueError("Project name must be unique.")

        self._projects[index].name = new_name

    def remove_project(self, index: int) -> None:
        """Delete a project and its tasks (cascade)."""
        if not (0 <= index < len(self._projects)):
            raise IndexError("Invalid project index.")
        del self._projects[index]

    def add_task_to_project(self, project_index: int, title: str, description: str) -> None:
        """Add a new task to a specific project."""
        if not (0 <= project_index < len(self._projects)):
            raise IndexError("Invalid project index.")

        project = self._projects[project_index]
        if len(project.tasks) >= self._max_tasks:
            raise OverflowError("Maximum number of tasks reached for this project.")

        title = title.strip()
        description = description.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if len(title) > self._max_task_name_length:
            raise ValueError(f"Task title cannot exceed {self._max_task_name_length} characters.")
        if not description:
            raise ValueError("Task description cannot be empty.")
        if len(description) > self._max_task_description_length:
            raise ValueError(f"Task description cannot exceed {self._max_task_description_length} characters.")

        project.tasks.append(Task(title=title, description=description))

    def update_task_status(self, project_index: int, task_index: int, new_status: str) -> None:
        """Update the status of a task in a project."""
        if not (0 <= project_index < len(self._projects)):
            raise IndexError("Invalid project index.")

        project = self._projects[project_index]
        if not (0 <= task_index < len(project.tasks)):
            raise IndexError("Invalid task index.")

        valid_status = {"todo", "doing", "done"}
        if new_status not in valid_status:
            raise ValueError("Invalid status value.")

        project.tasks[task_index].status = new_status

    def update_task_details(
        self, project_index: int, task_index: int, title: str, description: str, status: str
    ) -> None:
        """Update title, description, and status of a task."""
        if not (0 <= project_index < len(self._projects)):
            raise IndexError("Invalid project index.")

        project = self._projects[project_index]
        if not (0 <= task_index < len(project.tasks)):
            raise IndexError("Invalid task index.")

        title = title.strip()
        description = description.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if len(title) > self._max_task_name_length:
            raise ValueError(f"Task title cannot exceed {self._max_task_name_length} characters.")
        if not description:
            raise ValueError("Task description cannot be empty.")
        if len(description) > self._max_task_description_length:
            raise ValueError(f"Task description cannot exceed {self._max_task_description_length} characters.")

        valid_status = {"todo", "doing", "done"}
        if status not in valid_status:
            raise ValueError("Invalid status value.")

        project.tasks[task_index] = Task(title=title, description=description, status=status)

    def remove_task(self, project_index: int, task_index: int) -> None:
        """Delete a specific task from a project."""
        if not (0 <= project_index < len(self._projects)):
            raise IndexError("Invalid project index.")
        project = self._projects[project_index]
        if not (0 <= task_index < len(project.tasks)):
            raise IndexError("Invalid task index.")
        del project.tasks[task_index]
