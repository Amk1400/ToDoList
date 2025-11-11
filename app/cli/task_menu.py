from app.models.models import Detail, Project, Task
from app.services.task_service import TaskManager
from app.cli.entity_menu import EntityMenu
from app.exceptions.entity import (
    ValidationError,
    LimitExceededError,
    NotFoundError,
    AlreadyExistsError,
    StatusError,
)


class TaskMenu(EntityMenu[Task]):
    """Menu for managing tasks inside a project."""

    def __init__(self, task_manager: TaskManager, project: Project, parent_menu: EntityMenu) -> None:
        """Initialize the task menu.

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
        """Return additional info for display."""
        return f"[{entity.status}]"

    def _show_tasks(self) -> None:
        """Display all tasks in the project."""
        self._view_entities(self._project.tasks, "Task")

    def _create_task(self) -> None:
        """Add a new task using TaskManager."""
        try:
            detail = self._get_input_detail()
            self._task_manager.create_task(detail)
            self._project.tasks.append(self._task_manager.get_all_tasks()[-1])
            print("✅ Task created successfully.")
        except (ValidationError, LimitExceededError, AlreadyExistsError) as error:
            self._handle_error(error)

    def _update_task(self) -> None:
        """Update an existing task.

        Raises:
            ValidationError: If new data invalid.
            NotFoundError: If index invalid.
            StatusError: If status invalid.
        """
        tasks = self._project.tasks
        if not tasks:
            print("⚠ No tasks available.")
            return

        self._view_entities(tasks, "Task")
        try:
            index = int(input("Enter task number: ")) - 1
            title = input("Enter new title: ").strip()
            description = input("Enter new description: ").strip()
            detail = Detail(title=title, description=description)
            self._task_manager.update_task(index, detail)
            print("✅ Task updated successfully.")
        except (ValidationError, NotFoundError, StatusError, ValueError) as error:
            self._handle_error(error)

    def _delete_task(self) -> None:
        """Delete a task."""
        self._delete_entity(
            self._project.tasks,
            lambda idx: (self._task_manager.remove_task(idx), self._project.tasks.pop(idx)),
            "Task"
        )
