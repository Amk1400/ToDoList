from typing import List
from config import AppConfig
from models import Detail, Task, Project


class ProjectManager:
    """Manages all projects and their tasks."""

    def __init__(
        self,
        config: AppConfig
    ) -> None:
        """Initialize project manager with validation limits."""
        self._config = config
        self._projects: List[Project] = []

    def get_all_projects(self) -> List[Project]:
        """Return all projects."""
        return self._projects

    def create_project(self, detail: Detail) -> None:
        """Create a new project."""
        self._validate_project_fields(detail)
        if len(self._projects) >= self._max_projects:
            raise OverflowError("Maximum number of projects reached.")
        if any(p.detail.title == detail.title for p in self._projects):
            raise ValueError("Project title must be unique.")
        self._projects.append(Project(detail=detail))

    def update_project_name(self, index: int, new_title: str) -> None:
        """Rename a project."""
        project = self._get_project(index)
        if not new_title.strip():
            raise ValueError("Project title cannot be empty.")
        if any(p.detail.title == new_title for p in self._projects):
            raise ValueError("Project title must be unique.")
        if len(new_title.strip()) > self._max_name_length:
            raise ValueError(f"Title cannot exceed {self._max_name_length} characters.")
        project.detail.title = new_title.strip()

    def remove_project(self, index: int) -> None:
        """Remove a project."""
        project = self._get_project(index)
        self._projects.remove(project)

    def add_task_to_project(self, project_index: int, detail: Detail) -> None:
        """Add a new task to a project."""
        project = self._get_project(project_index)
        self._validate_task_fields(detail)
        if len(project.tasks) >= self._max_tasks:
            raise OverflowError("Maximum number of tasks reached.")
        project.tasks.append(Task(detail=detail))

    def update_task_status(self, project_index: int, task_index: int, new_status: str) -> None:
        """Update task status."""
        task = self._get_task(self._get_project(project_index), task_index)
        if new_status not in {"todo", "doing", "done"}:
            raise ValueError("Invalid task status. Must be one of: todo, doing, done.")
        task.status = new_status

    def update_task_details(self, project_index: int, task_index: int, detail: Detail, status: str) -> None:
        """Update all task details."""
        project = self._get_project(project_index)
        self._validate_task_fields(detail)
        if status not in {"todo", "doing", "done"}:
            raise ValueError("Invalid task status. Must be one of: todo, doing, done.")
        project.tasks[task_index].detail = detail
        project.tasks[task_index].status = status

    def remove_task(self, project_index: int, task_index: int) -> None:
        """Remove a task."""
        project = self._get_project(project_index)
        task = self._get_task(project, task_index)
        project.tasks.remove(task)

    def _get_project(self, index: int) -> Project:
        """Return a project by index."""
        if not (0 <= index < len(self._projects)):
            raise IndexError("Invalid project index.")
        return self._projects[index]

    def _get_task(self, project: Project, index: int) -> Task:
        """Return a task by index."""
        if not (0 <= index < len(project.tasks)):
            raise IndexError("Invalid task index.")
        return project.tasks[index]

    def _validate_project_fields(self, detail: Detail) -> None:
        """Validate project detail fields."""
        title, description = detail.title.strip(), detail.description.strip()
        if not title:
            raise ValueError("Project title cannot be empty.")
        if len(title) > self._max_name_length:
            raise ValueError(f"Project title cannot exceed {self._max_name_length} characters.")
        if not description:
            raise ValueError("Project description cannot be empty.")
        if len(description) > self._max_description_length:
            raise ValueError(f"Project description cannot exceed {self._max_description_length} characters.")

    def _validate_task_fields(self, detail: Detail) -> None:
        """Validate task detail fields."""
        title, description = detail.title.strip(), detail.description.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if len(title) > self._max_task_name_length:
            raise ValueError(f"Task title cannot exceed {self._max_task_name_length} characters.")
        if not description:
            raise ValueError("Task description cannot be empty.")
        if len(description) > self._max_task_description_length:
            raise ValueError(f"Task description cannot exceed {self._max_task_description_length} characters.")
