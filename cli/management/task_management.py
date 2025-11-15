from cli.management.entity_management import EntityManagementMenu
from service.task_manager import TaskManager
from models.models import Project

class TaskManagementMenu(EntityManagementMenu):
    """Task management menu for a specific project."""
    def __init__(self, task_manager: TaskManager, project: Project, parent_menu):
        super().__init__(task_manager, project, parent_menu)
        self._title = f"Task Management: {project.detail.title}"
