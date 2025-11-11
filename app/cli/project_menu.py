from typing import List
from app.models.models import Detail, Project
from app.services.project_service import ProjectManager
from app.cli.base_menu import BaseMenu
from app.cli.task_menu import TaskMenu
from app.exceptions.entity import (
    ValidationError,
    LimitExceededError,
    AlreadyExistsError,
    NotFoundError,
)


class ProjectMenu(BaseMenu):
    """Menu for managing projects."""

    def __init__(self, project_manager: ProjectManager, parent_menu: BaseMenu) -> None:
        """
        Initialize the project menu.

        Args:
            project_manager (ProjectManager): Handles project operations.
            parent_menu (BaseMenu): Parent menu for navigation.
        """
        super().__init__("Project Management", parent_menu)
        self._project_manager = project_manager
        self._setup_options()

    def _setup_options(self) -> None:
        """Register available project options."""
        self.add_option("1", self._view_projects)
        self.add_option("2", self._create_project)
        self.add_option("3", self._rename_project)
        self.add_option("4", self._delete_project)
        self.add_option("5", self._open_task_menu)
        self.add_option("6", self._go_back)

    def _view_projects(self) -> None:
        """Display all projects."""
        projects: List[Project] = self._project_manager.get_all_projects()
        if not projects:
            print("No projects available.")
            return
        for i, project in enumerate(projects, start=1):
            print(f"{i}. {project.detail.title} - {project.detail.description}")

    def _create_project(self) -> None:
        """Create a new project.

        Raises:
            ValidationError: If validation fails.
            LimitExceededError: If project limit is reached.
            AlreadyExistsError: If a project with the same title exists.
        """
        title = input("Enter project title: ").strip()
        description = input("Enter project description: ").strip()
        try:
            detail = Detail(title=title, description=description)
            self._project_manager.create_project(detail)
            print("✅ Project created successfully.")
        except (ValidationError, LimitExceededError, AlreadyExistsError) as error:
            print(f"❌ {error}")

    def _rename_project(self) -> None:
        """Rename an existing project.

        Raises:
            ValidationError: If title validation fails.
            NotFoundError: If project index is invalid.
        """
        self._view_projects()
        try:
            index = int(input("Enter project number: ")) - 1
            new_title = input("Enter new project title: ").strip()
            project = self._project_manager.get_all_projects()[index]
            updated_detail = Detail(title=new_title, description=project.detail.description)
            self._project_manager.update_project(index, updated_detail)
            print("✅ Project renamed successfully.")
        except (ValidationError, NotFoundError) as error:
            print(f"❌ {error}")

    def _delete_project(self) -> None:
        """Delete a project.

        Raises:
            NotFoundError: If project index is invalid.
        """
        self._view_projects()
        try:
            index = int(input("Enter project number: ")) - 1
            self._project_manager.remove_project(index)
            print("🗑️ Project deleted successfully.")
        except NotFoundError as error:
            print(f"❌ {error}")

    def _open_task_menu(self) -> None:
        """Open the task menu for a selected project.

        Raises:
            NotFoundError: If selected project index is invalid.
        """
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("No projects available.")
            return
        for i, project in enumerate(projects, start=1):
            print(f"{i}. {project.detail.title}")

        try:
            index = int(input("Enter project number: ")) - 1
            project = projects[index]
            task_manager = self._project_manager.get_task_manager()
            TaskMenu(task_manager, project, parent_menu=self).run()
        except (IndexError, NotFoundError) as error:
            print(f"❌ {error}")
