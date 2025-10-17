from models import Detail
from managers.task_manager import TaskManager


class TaskMenu:
    """Handles task-related operations within a project."""

    def __init__(self, task_manager: TaskManager) -> None:
        """Initialize with task manager."""
        self._task_manager = task_manager

    def run(self, project) -> None:
        """Run task menu for a project."""
        while True:
            print(f"\n--- TASK MENU ({project.detail.title}) ---")
            print("1. View Tasks")
            print("2. Add Task")
            print("3. Update Task")
            print("4. Delete Task")
            print("5. Back")

            choice = input("Choose an option: ").strip()
            actions = {
                "1": lambda: self._view_tasks(project),
                "2": lambda: self._add_task(project),
                "3": lambda: self._update_task(project),
                "4": lambda: self._delete_task(project),
            }

            if choice == "5":
                break
            action = actions.get(choice)
            action() if action else print("Invalid choice.")

    def _view_tasks(self, project) -> None:
        if not project.tasks:
            print("No tasks.")
            return
        for i, t in enumerate(project.tasks, start=1):
            print(f"{i}. {t.detail.title} [{t.status}] - {t.detail.description}")

    def _add_task(self, project) -> None:
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        try:
            self._task_manager.add_task(project, Detail(title=title, description=description))
            print("Task added.")
        except Exception as e:
            print(f"Error: {e}")

    def _update_task(self, project) -> None:
        self._view_tasks(project)
        try:
            index = int(input("Enter task number: ")) - 1
            new_status = input("Enter new status (todo/doing/done): ")
            self._task_manager.update_task(project, index, status=new_status)
            print("Task updated.")
        except Exception as e:
            print(f"Error: {e}")

    def _delete_task(self, project) -> None:
        self._view_tasks(project)
        try:
            index = int(input("Enter task number: ")) - 1
            self._task_manager.remove_task(project, index)
            print("Task deleted.")
        except Exception as e:
            print(f"Error: {e}")
