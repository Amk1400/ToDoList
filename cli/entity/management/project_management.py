from service.project_manager import ProjectManager
from cli.entity.management.entity_management import EntityManagementMenu

class ProjectManagementMenu(EntityManagementMenu):
    """Project management menu inheriting entity management."""
    def __init__(self, project_manager: ProjectManager, parent_menu):
        super().__init__(project_manager, parent_menu=parent_menu)
        self._title = "Project Management"
