from cli.entity.gateway.entity_gateway import EntityGateway
from models.models import Project
from service.project_manager import ProjectManager
from service.task_manager import TaskManager


class ProjectGateway(EntityGateway):
    """CLI gateway for project creation and editing."""

    def __init__(self, manager: ProjectManager) -> None:
        super().__init__(manager)

    def _fetch_optional_create(self) -> dict:
        return {}

    def _fetch_optional_edit(self, entity: Project) -> dict:
        return {}

    def get_task_manager(self) -> TaskManager:
        return self._manager.get_task_manager()