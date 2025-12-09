from typing import Dict

from api_cli.cli.fetcher import CliFetcher
from api_cli.gateway.entity_gateway import EntityGateway
from models.models import Task, Project
from service.task_manager import TaskManager


class TaskGateway(EntityGateway[Task]):
    """CLI gateway for task-related user interactions.

    Attributes:
        _manager (TaskManager): Task manager service.
        _parent_project (Project): Currently selected parent project.
        _fetcher (CliFetcher): CLI input fetcher instance.
    """

    def __init__(self, manager: TaskManager, parent_project: Project) -> None:
        """Initialize the task gateway with manager and parent project.

        Args:
            manager (TaskManager): Task manager service.
            parent_project (Project): Parent project for tasks.

        Returns:
            None: No value is returned.
        """
        super().__init__(manager)
        self._manager: TaskManager = manager
        self._parent_project: Project = parent_project
        self._manager.set_parent_project(parent_project)
        self._fetcher = CliFetcher(self._manager)

    def set_current_project(self, project: Project) -> None:
        """Set the current parent project context.

        Args:
            project (Project): New parent project.

        Returns:
            None: No value is returned.
        """
        self._parent_project = project
        self._manager.set_parent_project(project)

    def _fetch_optional_create(self) -> Dict:
        """Fetch optional task fields during creation.

        Returns:
            Dict: Optional task fields including deadline and status.
        """
        return {
            "deadline": self._fetcher.fetch_deadline(),
            "status": self._fetcher.fetch_status(),
        }

    def _fetch_optional_edit(self, entity: Task) -> Dict:
        """Fetch optional task fields during editing.

        Args:
            entity (Task): Target task entity.

        Returns:
            Dict: Optional task fields including deadline and status.
        """
        return {
            "deadline": self._fetcher.fetch_deadline(),
            "status": self._fetcher.fetch_status(),
        }
