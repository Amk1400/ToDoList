from typing import Optional
from datetime import date
from core.config import AppConfig
from models import Detail, Task, Project
from service.base_manager import BaseManager


class TaskManager(BaseManager[Task]):
    """Handles task-level operations for a project."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize task manager.

        Args:
            config (AppConfig): Application configuration.
        """
        super().__init__(config)

    def add_task(self, project: Project, detail: Detail, deadline: date) -> None:
        """Add a new task to a project.

        Args:
            project (Project): The project to add the task to.
            detail (Detail): Task detail.
            deadline (date): Task deadline.

        Raises:
            OverflowError: If project already has max tasks.
            ValueError: If validation fails.
        """
        self._validate_deadline(deadline)
        self._validate(detail)
        if len(project.tasks) >= self._config.max_tasks:
            raise OverflowError("Maximum number of tasks reached.")
        project.tasks.append(Task(detail=detail, deadline=deadline))

    def get_task(self, project: Project, task_index: int) -> Task:
        """Get a task by index."""
        return self.get_entity(project.tasks, task_index)

    def remove_task(self, project: Project, task_index: int) -> None:
        """Remove a task by index."""
        self.remove_entity(project.tasks, task_index)

    def update_task(
        self,
        project: Project,
        task_idx: int,
        detail: Optional[Detail] = None,
        deadline: Optional[date] = None,
        status: Optional[str] = None,
    ) -> None:
        """Update task details, deadline, or status.

        Args:
            project (Project): The project containing the task.
            task_idx (int): Task index.
            detail (Optional[Detail]): New detail, if updating.
            deadline (Optional[date]): New deadline, if updating.
            status (Optional[str]): New status, if updating.

        Raises:
            ValueError: If invalid status or past deadline.
        """
        task = self.get_entity(project.tasks, task_idx)

        if detail is not None:
            self.update_entity(project.tasks, task_idx, detail)

        if deadline is not None:
            self._validate_deadline(deadline)
            task.deadline = deadline

        if status is not None:
            if status not in {"todo", "doing", "done"}:
                raise ValueError("Invalid status. Must be one of: todo, doing, done.")
            task.status = status

    def _entity_name(self) -> str:
        return "Task"

    def _create_entity(self, detail: Detail) -> Task:
        raise NotImplementedError("Use add_task() for Task creation with deadline.")

    def _validate(self, detail: Detail) -> None:
        self._validate_detail(
            detail,
            self._config.max_task_name_length,
            self._config.max_task_description_length,
            "Task",
        )

    def _update_entity_detail(self, entity: Task, detail: Detail) -> None:
        entity.detail = detail
