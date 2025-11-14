from typing import Optional
from app.models.models import Task, Project, Detail, Status
from app.services.task_service import TaskManager
from app.cli.entity_menu import EntityMenu
from app.exceptions.entity import NotFoundError


class TaskMenu(EntityMenu[Task]):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: Optional[EntityMenu] = None) -> None:
        """Initialize task menu."""
        self._task_manager = task_manager
        self._project = project
        super().__init__(f"Task Management for {project.detail.title}", parent_menu)

    def _setup_options(self) -> None:
        """Register task menu options."""
        self.add_option("1", self._show_tasks)
        self.add_option("2", self._create_task)
        self.add_option("3", self._update_task)
        self.add_option("4", self._delete_task)
        self.add_option("5", self._go_back)

    def _show_tasks(self) -> None:
        """Display all tasks."""
        try:
            tasks = self._task_manager.list_tasks_for_project(self._project)
            self._view_entities(tasks, "Task")
        except NotFoundError as error:
            self._handle_error(error)
            return

    def _create_task(self) -> None:
        """Create a new task."""
        try:
            detail = self._get_input_detail()
            status = self._collect_task_status()
            from app.models.models import Task
            task = Task(detail=detail, status=status)
            self._task_manager.create_task_for_project(self._project, task, detail)
            print("✅ Task created successfully.")
        except Exception as error:
            self._handle_error(error)
            return

    def _update_task(self) -> None:
        """Update a task."""
        try:
            tasks = self._task_manager.list_tasks_for_project(self._project)
            self._view_entities(tasks, "Task")
            index = int(input("Enter task number to update: ")) - 1
            detail = self._get_input_detail()
            status = self._collect_task_status()
            self._task_manager.update_task_for_project(self._project, index, detail, status)
            print("✅ Task updated successfully.")
        except Exception as error:
            self._handle_error(error)
            return

    def _delete_task(self) -> None:
        """Delete a task."""
        try:
            tasks = self._task_manager.list_tasks_for_project(self._project)
            self._view_entities(tasks, "Task")
            index = int(input("Enter task number to delete: ")) - 1
            self._task_manager.remove_task_from_project(self._project, index)
            print("🗑️ Task deleted successfully.")
        except Exception as error:
            self._handle_error(error)
            return

    def _collect_task_status(self) -> Status:
        """Prompt user to input valid task status."""
        while True:
            raw_status = input("Enter status (todo/doing/done): ").strip().lower()
            try:
                return Status(raw_status)
            except ValueError:
                print("⚠ Invalid status. Please enter 'todo', 'doing', or 'done'.")
