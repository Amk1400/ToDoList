from typing import List
from app.models.models import Detail, Project
from app.services.project_service import ProjectManager
from app.cli.base_menu import BaseMenu
from app.cli.task_menu import TaskMenu
from app.exceptions.entity import ValidationError, NotFoundError, LimitExceededError


class ProjectMenu(BaseMenu):
    """Menu for managing project-related operations."""

    def __init__(self, project_manager: ProjectManager, parent_menu: BaseMenu) -> None:
        """Initialize the project menu.

        Args:
            project_manager (ProjectManager): Handles project-related operations.
            parent_menu (BaseMenu): Parent menu for navigation hierarchy.
        """
        super().__init__("Project Management", parent_menu)
        self._project_manager = project_manager
        self._setup_options()

    def _setup_options(self) -> None:
        """Define and register project menu options."""
        self.add_option("1", self._show_projects)
        self.add_option("2", self._create_project)
        self.add_option("3", self._rename_project)
        self.add_option("4", self._delete_project)
        self.add_option("5", self._open_task_menu)
        self.add_option("6", self._go_back)

    def _show_projects(self) -> None:
        """Display all projects."""
        projects = self._project_manager.get_all_projects()
        self._view_projects(projects)

    def _view_projects(self, projects: List[Project]) -> None:
        """Render a list of projects.

        Args:
            projects (List[Project]): The projects to display.
        """
        if not projects:
            print("⚠ No projects available.")
            return
        for index, project in enumerate(projects, start=1):
            print(f"{index}. {project.detail.title} - {project.detail.description}")

    def _create_project(self) -> None:
        """Create a project.

        Raises:
            ValidationError: If the project details are invalid.
            LimitExceededError: If the project limit is reached.
        """
        title = input("Enter project title: ").strip()
        description = input("Enter project description: ").strip()
        try:
            detail = Detail(title=title, description=description)
            self._project_manager.create_project(detail)
            print("✅ Project created successfully.")
        except (ValidationError, LimitExceededError) as error:
            print(f"❌ {error}")

    def _rename_project(self) -> None:
        """Rename a project.

        Raises:
            ValidationError: If validation fails.
            NotFoundError: If the project index is invalid.
        """
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("⚠ No projects available.")
            return

        self._view_projects(projects)
        try:
            index = int(input("Enter project number: ")) - 1
            new_title = input("Enter new project title: ").strip()
            project = projects[index]
            updated_detail = Detail(
                title=new_title, description=project.detail.description
            )
            self._project_manager.update_project(index, updated_detail)
            print("✅ Project renamed successfully.")
        except (ValidationError, NotFoundError, ValueError) as error:
            print(f"❌ {error}")

    def _delete_project(self) -> None:
        """Delete a project.

        Raises:
            NotFoundError: If the project index is invalid.
        """
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("⚠ No projects available.")
            return

        self._view_projects(projects)
        try:
            index = int(input("Enter project number: ")) - 1
            self._project_manager.remove_project(index)
            print("🗑️ Project deleted successfully.")
        except (NotFoundError, ValueError) as error:
            print(f"❌ {error}")

    def _open_task_menu(self) -> None:
        """Open the task menu for a selected project.

        Raises:
            NotFoundError: If the project index is invalid.
        """
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("⚠ No projects available.")
            return

        self._view_projects(projects)
        try:
            project_index = int(input("Enter project number: ")) - 1
            project = projects[project_index]
            task_manager = self._project_manager.get_task_manager()
            TaskMenu(task_manager, project, parent_menu=self).run()
        except (NotFoundError, ValueError) as error:
            print(f"❌ {error}")
