from typing import Optional
from app.models.models import Project, Detail
from app.services.project_service import ProjectManager
from app.cli.entity_menu import EntityMenu
from app.cli.task_menu import TaskMenu
from app.exceptions.entity import NotFoundError


class ProjectMenu(EntityMenu[Project]):
    """Menu for managing projects."""

    def __init__(self, project_manager: ProjectManager, parent_menu: Optional[EntityMenu] = None) -> None:
        """Initialize the project menu."""
        self._project_manager = project_manager
        super().__init__("Project Management", parent_menu)

    def _setup_options(self) -> None:
        """Register project options."""
        self.add_option("1", self._show_projects)
        self.add_option("2", self._create_project)
        self.add_option("3", self._rename_project)
        self.add_option("4", self._delete_project)
        self.add_option("5", self._open_task_menu)
        self.add_option("6", self._go_back)

    def _show_projects(self) -> None:
        """Display all projects."""
        try:
            projects = self._project_manager.list_entities()
            self._view_entities(projects, "Project")
        except NotFoundError as error:
            self._handle_error(error)
            return

    def _create_project(self) -> None:
        """Create a new project."""
        try:
            detail = self._get_input_detail()
            from app.models.models import Project
            project = Project(detail=detail)
            self._project_manager.create_entity(project, detail)
            print("✅ Project created successfully.")
        except Exception as error:
            self._handle_error(error)
            return

    def _rename_project(self) -> None:
        """Rename a project."""
        try:
            projects = self._project_manager.list_entities()
            self._view_entities(projects, "Project")
            index = int(input("Enter project number to rename: ")) - 1
            detail = self._get_input_detail()
            self._project_manager.update_entity(index, detail)
            print("✅ Project updated successfully.")
        except Exception as error:
            self._handle_error(error)
            return

    def _delete_project(self) -> None:
        """Delete a project."""
        try:
            projects = self._project_manager.list_entities()
            self._view_entities(projects, "Project")
            index = int(input("Enter project number to delete: ")) - 1
            self._project_manager.remove_entity(index)
            print("🗑️ Project deleted successfully.")
        except Exception as error:
            self._handle_error(error)
            return

    def _open_task_menu(self) -> None:
        """Open the task menu for a project."""
        try:
            projects = self._project_manager.list_entities()
            self._view_entities(projects, "Project")
            index = int(input("Enter project number: ")) - 1
            project = projects[index]
            task_manager = self._project_manager.get_task_manager()
            TaskMenu(task_manager, project, parent_menu=self).run()
        except Exception as error:
            self._handle_error(error)
            return
