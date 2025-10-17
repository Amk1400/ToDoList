from models import Detail
from managers.project_manager import ProjectManager
from menus.task_menu import TaskMenu


class ProjectMenu:
    """Handles project-related operations."""

    def __init__(self, project_manager: ProjectManager) -> None:
        """Initialize with project manager."""
        self._project_manager = project_manager
        self._task_menu = TaskMenu(project_manager.get_task_manager())

    def run(self) -> None:
        """Run project management menu."""
        while True:
            print("\n--- PROJECT MENU ---")
            print("1. View Projects")
            print("2. Create Project")
            print("3. Rename Project")
            print("4. Delete Project")
            print("5. Manage Tasks")
            print("6. Back")

            choice = input("Choose an option: ").strip()
            actions = {
                "1": self._view_projects,
                "2": self._create_project,
                "3": self._rename_project,
                "4": self._delete_project,
                "5": self._open_task_menu,
            }

            if choice == "6":
                break
            action = actions.get(choice)
            action() if action else print("Invalid choice.")

    def _view_projects(self) -> None:
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("No projects available.")
            return
        for i, p in enumerate(projects, start=1):
            print(f"{i}. {p.detail.title} - {p.detail.description}")

    def _create_project(self) -> None:
        title = input("Enter project title: ")
        description = input("Enter project description: ")
        try:
            self._project_manager.create_project(Detail(title=title, description=description))
            print("Project created.")
        except Exception as e:
            print(f"Error: {e}")

    def _rename_project(self) -> None:
        self._view_projects()
        try:
            index = int(input("Enter project number: ")) - 1
            new_title = input("Enter new title: ")
            self._project_manager.update_project(index, Detail(title=new_title, description=""))
            print("Project renamed.")
        except Exception as e:
            print(f"Error: {e}")

    def _delete_project(self) -> None:
        self._view_projects()
        try:
            index = int(input("Enter project number: ")) - 1
            self._project_manager.remove_project(index)
            print("Project deleted.")
        except Exception as e:
            print(f"Error: {e}")

    def _open_task_menu(self) -> None:
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("No projects available.")
            return
        try:
            index = int(input("Enter project number: ")) - 1
            project = projects[index]
            self._task_menu.run(project)
        except Exception as e:
            print(f"Error: {e}")
