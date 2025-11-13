from typing import Optional, Tuple

from app.models.models import Project, Task, Status, Detail
from app.services.task_service import TaskManager
from app.cli.entity_menu import EntityMenu


class TaskMenu(EntityMenu[Task]):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: EntityMenu) -> None:
        """Initialize task menu."""
        self._task_manager: TaskManager = task_manager
        self._project: Project = project
        super().__init__(
            f"Task Management for {project.detail.title}",
            parent_menu,
            entity_manager=self._task_manager
        )

    def _setup_options(self) -> None:
        """Register task menu options."""
        self.add_option("1", self._show_tasks)
        self.add_option("2", self._create_task)
        self.add_option("3", self._update_task)
        self.add_option("4", self._delete_task)
        self.add_option("5", self._go_back)

    def _show_tasks(self) -> None:
        """Display all tasks."""
        self._view_entities(self._project.tasks, "Task")

    def _create_task(self) -> None:
        """Create a new task."""
        self._create_entity(self._project, "Task")

    def _update_task(self) -> None:
        """Update a task detail."""
        self._update_entity_by_index(self._project, "Task")

    def _delete_task(self) -> None:
        """Delete a task."""
        self._delete_entity_by_index(self._project, "Task")

    def _collect_task_status(self) -> Status:
        """Prompt user to input valid task status."""
        while True:
            raw_status = input("Enter preferred status (todo/doing/done): ").strip().lower()
            try:
                return Status(raw_status)
            except ValueError:
                print("⚠ Invalid status. Please enter 'todo', 'doing', or 'done'.")

    def _collect_update_data(self, parent: object, entity_name: str) -> Tuple[int, Detail, Optional[Status]]:
        """Collect index, detail, and optional status for update."""
        index = self._select_entity_index(parent, entity_name)
        detail = self._get_input_detail()
        status: Optional[Status] = self._collect_task_status() if entity_name == "Task" else None
        return index, detail, status