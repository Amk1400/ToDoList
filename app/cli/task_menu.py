from app.models.models import Project, Task
from app.services.task_service import TaskManager
from app.cli.entity_menu import EntityMenu


class TaskMenu(EntityMenu[Task]):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: EntityMenu) -> None:
        """Initialize task menu.

        Args:
            task_manager (TaskManager): Handles task operations.
            project (Project): The project containing tasks.
            parent_menu (EntityMenu): Parent menu for navigation.
        """
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

    def _get_extra_info(self, entity: Task) -> str:
        """Return additional info for display.

        Args:
            entity (Task): Task to describe.

        Returns:
            str: Status info.
        """
        return f"[{entity.status}]"

    def _show_tasks(self) -> None:
        """Display all tasks."""
        self._view_entities(self._project.tasks, "Task")

    def _create_task(self) -> None:
        """Create a new task."""
        self._create_entity(
            lambda detail: self._task_manager.create_task_for_project(self._project, detail),
            "Task"
        )

    def _update_task(self) -> None:
        """Update a task detail."""
        self._update_entity(
            self._project.tasks,
            self._task_manager.update_task,
            "Task"
        )

    def _delete_task(self) -> None:
        """Delete a task."""
        self._delete_entity(
            self._project.tasks,
            self._task_manager.remove_task,
            "Task"
        )
