from app.models.models import Project
from app.services.project_service import ProjectManager
from app.cli.task_menu import TaskMenu
from app.cli.entity_menu import EntityMenu
from app.exceptions.entity import NotFoundError


class ProjectMenu(EntityMenu[Project]):
    """Menu for managing projects."""

    def __init__(self, project_manager: ProjectManager, parent_menu: EntityMenu) -> None:
        """Initialize the project menu.

        Args:
            project_manager (ProjectManager): Handles project operations.
            parent_menu (EntityMenu): Parent menu for navigation.
        """
        self._project_manager: ProjectManager = project_manager
        super().__init__("Project Management", parent_menu)

    def _setup_options(self) -> None:
        """Register project options."""
        self.add_option("1", self._show_projects)
        self.add_option("2", self._create_project)
        self.add_option("3", self._rename_project)
        self.add_option("4", self._delete_project)
        self.add_option("5", self._open_task_menu)
        self.add_option("6", self._go_back)

    def _get_extra_info(self, entity: Project) -> str:
        """Return project info.

        Args:
            entity (Project): Project entity.

        Returns:
            str: Empty string for consistency.
        """
        return ""

    def _show_projects(self) -> None:
        """Display all projects."""
        projects = self._project_manager.get_all_entities()
        self._view_entities(projects, "Project")

    def _create_project(self) -> None:
        """Create a new project."""
        self._create_entity(
            lambda detail: self._project_manager.create_entity(None, detail),
            "Project"
        )

    def _rename_project(self) -> None:
        """Rename a project."""
        projects = self._project_manager.get_all_entities()
        self._update_entity(
            projects,
            lambda index, detail: self._project_manager.update_entity_by_index(None, index, detail),
            "Project"
        )

    def _delete_project(self) -> None:
        """Delete a project."""
        projects = self._project_manager.get_all_entities()
        self._delete_entity(
            projects,
            lambda index: self._project_manager.remove_entity_by_index(None, index),
            "Project"
        )

    def _open_task_menu(self) -> None:
        """Open the task menu for a project."""
        projects = self._project_manager.get_all_entities()
        try:
            self._view_entities(projects, "Project")
            index = int(input("Enter project number: ")) - 1
            project = projects[index]
            task_manager = self._project_manager.get_task_manager()
            TaskMenu(task_manager, project, parent_menu=self).run()
        except (NotFoundError, ValueError) as error:
            self._handle_error(error)
