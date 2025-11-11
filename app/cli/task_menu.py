from typing import List
from app.models.models import Detail, Project, Task
from app.services.task_service import TaskManager
from app.cli.base_menu import BaseMenu
from app.exceptions.entity import ValidationError, LimitExceededError, NotFoundError, StatusError


class TaskMenu(BaseMenu):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: BaseMenu) -> None:
        """
        Initialize the task menu.

        Args:
            task_manager (TaskManager): Handles task operations.
            project (Project): The project containing tasks.
            parent_menu (BaseMenu): Parent menu for navigation.
        """
        super().__init__(f"Task Management for {project.detail.title}", parent_menu)
        self._task_manager = task_manager
        self._project = project
        self._setup_options()

    def _setup_options(self) -> None:
        """Register available task options."""
        self.add_option("1", self._show_tasks)
        self.add_option("2", self._add_task)
        self.add_option("3", self._update_task)
        self.add_option("4", self._delete_task)
        self.add_option("5", self._go_back)

    def _show_tasks(self) -> None:
        """Display all tasks for the project."""
        self._view_tasks(self._project.tasks)

    def _view_tasks(self, tasks: List[Task]) -> None:
        """Render a list of tasks.

        Args:
            tasks (List[Task]): The tasks to display.
        """
        if not tasks:
            print("⚠ No tasks available.")
            return
        for i, task in enumerate(tasks, start=1):
            print(f"{i}. {task.detail.title} [{task.status}] - {task.detail.description}")

    def _add_task(self) -> None:
        """Add a new task.

        Raises:
            ValidationError: If validation fails.
            LimitExceededError: If task limit is reached.
        """
        title = input("Enter task title: ").strip()
        description = input("Enter task description: ").strip()
        try:
            detail = Detail(title=title, description=description)
            self._task_manager.add_task(self._project, detail)
            print("✅ Task added successfully.")
        except (ValidationError, LimitExceededError) as error:
            print(f"❌ {error}")

    def _update_task(self) -> None:
        """Update an existing task.

        Raises:
            ValidationError: If new data is invalid.
            NotFoundError: If task index is invalid.
            StatusError: If task status is invalid.
        """
        self._view_tasks(self._project.tasks)
        try:
            index = int(input("Enter task number: ")) - 1
            title = input("Enter new title: ").strip()
            description = input("Enter new description: ").strip()
            status = input("Enter new status (todo/doing/done): ").strip()
            detail = Detail(title=title, description=description)
            self._task_manager.update_task(self._project, index, detail, status)
            print("✅ Task updated successfully.")
        except (ValidationError, NotFoundError, StatusError, ValueError) as error:
            print(f"❌ {error}")

    def _delete_task(self) -> None:
        """Delete a task.

        Raises:
            NotFoundError: If task index is invalid.
        """
        self._view_tasks(self._project.tasks)
        try:
            index = int(input("Enter task number: ")) - 1
            self._task_manager.remove_task(self._project, index)
            print("🗑️ Task deleted successfully.")
        except (NotFoundError, ValueError) as error:
            print(f"❌ {error}")
