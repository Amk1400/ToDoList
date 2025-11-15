from datetime import datetime
from service.task_manager import TaskManager
from models.models import Detail, Project
from cli.base_menu import BaseMenu


class TaskManagementMenu(BaseMenu):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: BaseMenu) -> None:
        """Initialize task menu.

        Args:
            task_manager (TaskManager): Task manager instance.
            project (Project): Target project.
            parent_menu (BaseMenu): Parent menu reference.
        """
        super().__init__(f"Task Menu: {project.detail.title}", parent_menu)
        self._task_manager = task_manager
        self._project = project
        self._setup_options()

    def _setup_options(self) -> None:
        """Define menu options."""
        self.add_option("1", self._view_tasks)
        self.add_option("2", self._add_task)
        self.add_option("3", self._update_task)
        self.add_option("4", self._delete_task)
        self.add_option("5", self._go_back)

    def _view_tasks(self) -> None:
        """View tasks."""
        if not self._project.tasks:
            print("No tasks available.")
            return
        for i, task in enumerate(self._project.tasks, start=1):
            print(f"{i}. {task.detail.title} [{task.status}] - {task.detail.description} (Due: {task.deadline})")

    def _add_task(self) -> None:
        """Add task."""
        try:
            title = input("Enter task title: ").strip()
            description = input("Enter task description: ").strip()
            deadline_str = input("Enter deadline (YYYY-MM-DD): ").strip()
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            self._task_manager.add_task(self._project, Detail(title, description), deadline)
            print("Task added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def _update_task(self) -> None:
        """Update task."""
        self._view_tasks()
        try:
            index = int(input("Enter task number: ")) - 1
            title = input("Enter new title: ").strip()
            description = input("Enter new description: ").strip()
            deadline_str = input("Enter new deadline (YYYY-MM-DD): ").strip()
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
            status = input("Enter new status (todo/doing/done): ").strip()
            self._task_manager.update_task(
                self._project, index, Detail(title, description), deadline, status
            )
            print("Task updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def _delete_task(self) -> None:
        """Delete task."""
        self._view_tasks()
        try:
            index = int(input("Enter task number: ")) - 1
            self._task_manager.remove_task(self._project, index)
            print("Task deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")
