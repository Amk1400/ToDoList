from cli.fetcher import CliFetcher
from models.models import Task, Project
from service.task_manager import TaskManager
from cli.gateway.entity_gateway import EntityGateway

class TaskGateway(EntityGateway):
    """Gateway for fetching task inputs from CLI to Service."""

    def __init__(self, manager: TaskManager, project: Project) -> None:
        super().__init__(manager)
        self._manager: TaskManager = manager
        self._project: Project = project
        self._manager.set_current_project(project)
        self._fetcher = CliFetcher(self._manager)

    def set_current_project(self, project: Project) -> None:
        """Set a new current project and update manager's entity list."""
        self._project = project
        self._manager.set_current_project(project)

    def _fetch_optional_create(self) -> dict:
        """Fetch optional fields during task creation (deadline)."""
        return {"deadline": self._fetcher.fetch_deadline(), "status": self._fetcher.fetch_status()}

    def _fetch_optional_edit(self, entity: Task) -> dict:
        """Fetch optional fields during task editing (deadline, status)."""
        return {"deadline": self._fetcher.fetch_deadline(), "status": self._fetcher.fetch_status()}