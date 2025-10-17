from typing import List, Optional
from config import AppConfig
from models import Detail, Task, Project
from managers.base_manager import BaseManager


class TaskManager(BaseManager[Task]):
    """Manager class responsible for handling all task-related operations."""

    def __init__(self, config: AppConfig) -> None:
        """Initialize the task manager.

        Args:
            config (AppConfig): Configuration object defining validation limits.
        """
        super().__init__(config)

    def add_task(self, project: Project, detail: Detail) -> None:
        """Add a new task to the given project.

        Args:
            project (Project): The project to which the task is added.
            detail (Detail): The title and description of the new task.

        Raises:
            OverflowError: If the maximum number of tasks is reached.
            ValueError: If validation of task details fails.
        """
        self.create(project.tasks, detail, self._config.max_tasks)

    def get_task(self, project: Project, task_index: int) -> Task:
        """Retrieve a task by its index.

        Args:
            project (Project): The project containing the task.
            task_index (int): The index of the task to retrieve.

        Returns:
            Task: The task object at the given index.

        Raises:
            IndexError: If the task index is invalid.
        """
        return self.get_entity(project.tasks, task_index)

    def remove_task(self, project: Project, task_index: int) -> None:
        """Remove a task from a given project.

        Args:
            project (Project): The project containing the task.
            task_index (int): The index of the task to remove.

        Raises:
            IndexError: If the task index is invalid.
        """
        self.remove_entity(project.tasks, task_index)

    def update_task(
        self,
        project: Project,
        task_idx: int,
        detail: Optional[Detail] = None,
        status: Optional[str] = None,
    ) -> None:
        """Update a task’s details and/or status.

        Args:
            project (Project): The project containing the task.
            task_idx (int): The index of the task to update.
            detail (Optional[Detail]): New detail object (title, description).
            status (Optional[str]): New status value ("todo", "doing", "done").

        Raises:
            ValueError: If the provided status is invalid.
            IndexError: If the task index is invalid.
        """
        task = self.get_entity(project.tasks, task_idx)

        if detail is not None:
            self.update_entity(project.tasks, task_idx, detail)

        if status is not None:
            if status not in {"todo", "doing", "done"}:
                raise ValueError("Invalid task status. Must be one of: todo, doing, done.")
            task.status = status

    def _entity_name(self) -> str:
        """Return the entity name for display/logging.

        Returns:
            str: The string 'Task'.
        """
        return "Task"

    def _create_entity(self, detail: Detail) -> Task:
        """Factory method to create a new task.

        Args:
            detail (Detail): The task's title and description.

        Returns:
            Task: A new task instance.
        """
        return Task(detail=detail)

    def _validate(self, detail: Detail) -> None:
        """Validate task details according to config limits.

        Args:
            detail (Detail): The detail object to validate.

        Raises:
            ValueError: If validation of title or description fails.
        """
        self._validate_detail(
            detail,
            self._config.max_task_name_length,
            self._config.max_task_description_length,
            "Task",
        )

    def _update_entity_detail(self, entity: Task, detail: Detail) -> None:
        """Apply updated detail data to a task entity.

        Args:
            entity (Task): The task being updated.
            detail (Detail): The new detail data.
        """
        entity.detail = detail
