from typing import Dict

from api_cli.cli.fetcher import CliFetcher
from api_cli.gateway.entity_gateway import EntityGateway
from models.models import Task, Project
from service.task_manager import TaskManager


class TaskGateway(EntityGateway[Task]):
    """Gateway for fetching task inputs from CLI to Service."""

    def __init__(self, manager: TaskManager, parent_project: Project) -> None:
        super().__init__(manager)
        self._manager: TaskManager = manager
        self._parent_project: Project = parent_project
        self._manager.set_parent_project(parent_project)
        self._fetcher = CliFetcher(self._manager)

    def set_current_project(self, project: Project) -> None:
        """Set a new current project and update manager's entity list."""
        self._parent_project = project
        self._manager.set_parent_project(project)

    def _fetch_optional_create(self) -> Dict:
        """Fetch optional fields during task creation (deadline, status)."""
        return {
            "deadline": self._fetcher.fetch_deadline(),
            "status": self._fetcher.fetch_status()
        }

    def _fetch_optional_edit(self, entity: Task) -> Dict:
        """Fetch optional fields during task editing (deadline, status)."""
        return {
            "deadline": self._fetcher.fetch_deadline(),
            "status": self._fetcher.fetch_status()
        }
