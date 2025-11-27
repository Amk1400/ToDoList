from cli.entity.gateway.entity_gateway import EntityGateway
from models.models import Project, Detail
from service.project_manager import ProjectManager
from service.task_manager import TaskManager


class ProjectGateway(EntityGateway):
    """Gateway for fetching project inputs from CLI to Service."""

    def __init__(self, manager: ProjectManager):
        """Initialize with ProjectManager."""
        super().__init__(manager)


    def _fetch_deadline(self) -> dict:
        """No optional fields for project creation."""
        return {}

    def _fetch_deadline_and_status(self, entity: Project) -> dict:
        """No optional fields for project edition."""
        return {}

    def _apply_create(self, detail: Detail, optional_args: dict) -> None:
        """Create project using service manager."""
        self._manager.add_entity(detail)

    def _apply_edit(self, entity: Project, detail: Detail, optional_args: dict) -> None:
        """Edit project using service manager."""
        # Find index of project in manager list
        projects = self._manager.get_entities()
        try:
            idx = projects.index(entity)
        except ValueError:
            print("Project not found.")
            return
        self._manager.update_project(idx, detail)

    def get_task_manager(self) -> TaskManager:
        return self._manager.get_task_manager()