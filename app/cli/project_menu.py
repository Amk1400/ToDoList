from app.models.models import Detail, Project
from app.services.project_service import ProjectManager
from app.cli.task_menu import TaskMenu
from app.cli.entity_menu import EntityMenu
from app.exceptions.entity import ValidationError, NotFoundError


class ProjectMenu(EntityMenu[Project]):
    """Menu for managing projects."""

    def __init__(self, project_manager: ProjectManager, parent_menu: EntityMenu) -> None:
        """Initialize the project menu.

        Args:
            project_manager (ProjectManager): Handles project operations.
            parent_menu (EntityMenu): Parent menu for navigation.
        """
        self._project_manager = project_manager
        super().__init__("Project Management", parent_menu)

    def _setup_options(self) -> None:
        """Register project menu options."""
        self.add_option("1", self._show_projects)
        self.add_option("2", self._create_project)
        self.add_option("3", self._rename_project)
        self.add_option("4", self._delete_project)
        self.add_option("5", self._open_task_menu)
        self.add_option("6", self._go_back)

    def _get_extra_info(self, entity: Project) -> str:
        """Return additional display info for projects."""
        return ""

    def _show_projects(self) -> None:
        """Display all projects."""
        projects = self._project_manager.get_all_projects()
        self._view_entities(projects, "Project")

    def _create_project(self) -> None:
        """Create a new project."""
        self._create_entity(self._project_manager.create_project, "Project")

    def _rename_project(self) -> None:
        """Rename a project.

        Raises:
            ValidationError: If detail invalid.
            NotFoundError: If index invalid.
        """
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("⚠ No projects available.")
            return

        self._view_entities(projects, "Project")
        try:
            index = int(input("Enter project number: ")) - 1
            new_title = input("Enter new project title: ").strip()
            project = projects[index]
            updated_detail = Detail(title=new_title, description=project.detail.description)
            self._project_manager.update_project(index, updated_detail)
            print("✅ Project renamed successfully.")
        except (ValidationError, NotFoundError, ValueError) as error:
            self._handle_error(error)

    def _delete_project(self) -> None:
        """Delete a project."""
        projects = self._project_manager.get_all_projects()
        self._delete_entity(
            projects,
            lambda idx: self._project_manager.remove_project(idx),
            "Project"
        )

    def _open_task_menu(self) -> None:
        """Open the task menu for a selected project."""
        projects = self._project_manager.get_all_projects()
        if not projects:
            print("⚠ No projects available.")
            return

        self._view_entities(projects, "Project")
        try:
            index = int(input("Enter project number: ")) - 1
            project = projects[index]
            task_manager = self._project_manager.get_task_manager()
            TaskMenu(task_manager, project, parent_menu=self).run()
        except (NotFoundError, ValueError) as error:
            self._handle_error(error)
