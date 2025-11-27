from typing import Dict
from cli.gateway.entity_gateway import EntityGateway
from models.models import Project
from service.task_manager import TaskManager


class ProjectGateway(EntityGateway[Project]):
    """Gateway for project operations."""

    def _fetch_optional_create(self) -> Dict:
        return {}

    def _fetch_optional_edit(self, entity: Project) -> Dict:
        return {}

    def get_task_manager(self) -> TaskManager:
        """Return the TaskManager for this project."""
        return self._manager.get_task_manager()