from typing import List
from models import Detail, Project
from managers.project_manager import ProjectManager
from menus.base_menu import BaseMenu
from menus.task_menu import TaskMenu


class ProjectMenu(BaseMenu):
    """Menu for managing project-related operations."""

    def __init__(self, project_manager: ProjectManager, parent_menu: BaseMenu) -> None:
        """Initialize the project menu.

        Args:
            project_manager (ProjectManager): Manages project-related logic.
            parent_menu (BaseMenu): Reference to the parent menu for navigation.
        """
        super().__init__("Project Management", parent_menu)
        self._project_manager = project_manager
        self._setup_options()

    def _setup_options(self) -> None:
        """Define and register project menu options."""
        self.add_option("1", self._view_projects)
        self.add_option("2", self._create_project)
        self.add_option("3", self._rename_project)
        self.add_option("4", self._delete_project)
        self.add_option("5", self._open_task_menu)
        self.add_option("6", self._go_back)

    def _view_projects(self) -> None:
        """Display all available projects."""
        projects: List[Project] = self._project_manager.get_all_projects()
        if not projects:
            print("No projects available.")
            return
        for index, project in enumerate(projects, start=1):
            print(f"{index}. {project.detail.title} - {project.detail.description}")

    def _create_project(self) -> None:
        """Prompt user for project details and create a new project.

        Raises:
            Exception: If project creation fails due to validation or capacity limits.
        """
        title = input("Enter project title: ").strip()
        description = input("Enter project description: ").strip()
        try:
            detail = Detail(title=title, description=description)
            self._project_manager.create_project(detail)
            print("✅ Project created successfully.")
        except Exception as error:
            print(f"❌ Error: {error}")

    def _rename_project(self) -> None:
        """Rename an existing project.

        Raises:
            Exception: If project index is invalid or update fails.
        """
        self._view_projects()
        try:
            index = int(input("Enter project number: ")) - 1
            new_title = input("Enter new project title: ").strip()
            project = self._project_manager.get_all_projects()[index]
            updated_detail = Detail(title=new_title, description=project.detail.description)
            self._project_manager.update_project(index, updated_detail)
            print("✅ Project renamed successfully.")
        except Exception as error:
            print(f"❌ Error: {error}")

    def _delete_project(self) -> None:
        """Delete a project by user selection.

        Raises:
            Exception: If project index is invalid or deletion fails.
        """
        self._view_projects()
        try:
            index = int(input("Enter project number: ")) - 1
            self._project_manager.remove_project(index)
            print("🗑️ Project deleted successfully.")
        except Exception as error:
            print(f"❌ Error: {error}")

    def _open_task_menu(self) -> None:
        """Open the task management menu for a selected project.

        Raises:
            Exception: If project selection or task menu initialization fails.
        """
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("No projects available.")
            return

        for index, project in enumerate(projects, start=1):
            print(f"{index}. {project.detail.title}")

        try:
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]
            task_manager = self._project_manager.get_task_manager()
            TaskMenu(task_manager, project, parent_menu=self).run()
        except Exception as error:
            print(f"❌ Error: {error}")
