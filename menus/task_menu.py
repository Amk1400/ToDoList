from managers.task_manager import TaskManager
from models import Detail, Project
from menus.base_menu import BaseMenu


class TaskMenu(BaseMenu):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: BaseMenu) -> None:
        """Initialize the task menu.

        Args:
            task_manager (TaskManager): Manager responsible for task operations.
            project (Project): The project that contains the tasks.
            parent_menu (BaseMenu): Reference to the parent menu.
        """
        super().__init__(f"Task Management for {project.detail.title}", parent_menu)
        self._task_manager: TaskManager = task_manager
        self._project: Project = project
        self._setup_options()

    def _setup_options(self) -> None:
        """Define menu options."""
        self.add_option("1", self._view_tasks)
        self.add_option("2", self._add_task)
        self.add_option("3", self._update_task)
        self.add_option("4", self._delete_task)
        self.add_option("5", self._go_back)

    def _view_tasks(self) -> None:
        """View tasks.

        Raises:
            Exception: If task list retrieval fails unexpectedly.
        """
        if not self._project.tasks:
            print("No tasks available.")
            return
        for i, task in enumerate(self._project.tasks, start=1):
            print(f"{i}. {task.detail.title} [{task.status}] - {task.detail.description}")

    def _add_task(self) -> None:
        """Add task.

        Raises:
            ValueError: If task title or description is invalid.
            OverflowError: If task limit is exceeded.
        """
        title = input("Enter task title: ").strip()
        description = input("Enter task description: ").strip()
        try:
            self._task_manager.add_task(self._project, Detail(title=title, description=description))
            print("Task added successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def _update_task(self) -> None:
        """Edit Task.

        Raises:
            IndexError: If selected task index is invalid.
            ValueError: If provided data is invalid.
        """
        self._view_tasks()
        try:
            index = int(input("Enter task number: ")) - 1
            title = input("Enter new title: ").strip()
            description = input("Enter new description: ").strip()
            status = input("Enter new status (todo/doing/done): ").strip()
            self._task_manager.update_task(self._project, index, Detail(title, description), status)
            print("Task updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def _delete_task(self) -> None:
        """Remove task.

        Raises:
            IndexError: If selected task index is invalid.
        """
        self._view_tasks()
        try:
            index = int(input("Enter task number: ")) - 1
            self._task_manager.remove_task(self._project, index)
            print("Task deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")
