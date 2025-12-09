from typing import Dict

from api_cli.gateway.entity_gateway import EntityGateway
from models.models import Project
from service.task_manager import TaskManager


class ProjectGateway(EntityGateway[Project]):
    """CLI gateway for project-related operations.

    Attributes:
        _config (Any): Application configuration object.
        _db (Any): Database dependency instance.
    """

    def __init__(self, manager, config, db) -> None:
        """Initialize the project gateway.

        Args:
            manager (Any): Project manager service.
            config (Any): Application configuration.
            db (Any): Database dependency.

        Returns:
            None: No value is returned.
        """
        super().__init__(manager)
        self._config = config
        self._db = db

    def _fetch_optional_create(self) -> Dict:
        """Fetch optional fields during project creation.

        Returns:
            Dict: Empty optional fields mapping.
        """
        return {}

    def _fetch_optional_edit(self, entity: Project) -> Dict:
        """Fetch optional fields during project editing.

        Args:
            entity (Project): Target project entity.

        Returns:
            Dict: Empty optional fields mapping.
        """
        return {}

    def get_task_manager(self, project: Project) -> TaskManager:
        """Get a task manager associated with a project.

        Args:
            project (Project): Target project entity.

        Returns:
            TaskManager: Task manager bound to the given project.
        """
        return self._manager.get_task_manager(project)
