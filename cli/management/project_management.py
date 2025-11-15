from service.project_manager import ProjectManager
from cli.base_menu import BaseMenu


class ProjectManagementMenu(BaseMenu):
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
        """
        TODO here i want 3 options
        1. show and modify which inherits from showentities and modify in entitymanagement
        2. create  which inherits from create entity in entity management
        3. back which enherits from back of basemenu
        """
        ...
