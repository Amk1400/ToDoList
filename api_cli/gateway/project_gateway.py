from typing import Dict

from api_cli.gateway.entity_gateway import EntityGateway
from models.models import Project
from service.task_manager import TaskManager


class ProjectGateway(EntityGateway[Project]):
    """Gateway for project operations."""

    def __init__(self, manager, config, db) -> None:
        super().__init__(manager)
        self._config = config
        self._db = db

    def _fetch_optional_create(self) -> Dict:
        return {}

    def _fetch_optional_edit(self, entity: Project) -> Dict:
        return {}

    def get_task_manager(self, project: Project) -> TaskManager:
        """Return TaskManager for the given project, creating if necessary."""
        return self._manager.get_task_manager(project)
