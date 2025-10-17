from config import AppConfig
from models import Project, Detail, Task


class TaskManager:
    """Handles CRUD operations for tasks within projects."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize task manager."""
        self._config = config

    def add_task(self, project: Project, detail: Detail) -> None:
        """Add a new task to a project."""
        self._validate_task_details(detail)
        if len(project.tasks) >= self._config.max_tasks:
            raise OverflowError("Maximum number of tasks reached.")
        project.tasks.append(Task(detail=detail))

    def update_task_status(self, project: Project, task_index: int, new_status: str) -> None:
        """Update a task's status."""
        task = self._get_task(project, task_index)
        if new_status not in {"todo", "doing", "done"}:
            raise ValueError("Invalid task status. Must be one of: todo, doing, done.")
        task.status = new_status

    def update_task_details(self, project: Project, task_index: int, detail: Detail, status: str) -> None:
        """Update all task details."""
        self._validate_task_details(detail)
        if status not in {"todo", "doing", "done"}:
            raise ValueError("Invalid task status. Must be one of: todo, doing, done.")
        task = self._get_task(project, task_index)
        task.detail = detail
        task.status = status

    def remove_task(self, project: Project, task_index: int) -> None:
        """Remove a task."""
        task = self._get_task(project, task_index)
        project.tasks.remove(task)

    def _get_task(self, project: Project, index: int) -> Task:
        """Return a task by index."""
        if not (0 <= index < len(project.tasks)):
            raise IndexError("Invalid task index.")
        return project.tasks[index]

    def _validate_task_details(self, detail: Detail) -> None:
        """Validate task detail fields."""
        title, description = detail.title.strip(), detail.description.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if len(title) > self._config.max_task_name_length:
            raise ValueError(
                f"Task title cannot exceed {self._config.max_task_name_length} characters."
            )
        if not description:
            raise ValueError("Task description cannot be empty.")
        if len(description) > self._config.max_task_description_length:
            raise ValueError(
                f"Task description cannot exceed {self._config.max_task_description_length} characters."
            )
