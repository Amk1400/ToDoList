from fastapi import APIRouter
from service.project_manager import ProjectManager

from ..tasks.getters import register_task_getters
from ..tasks.posters import register_task_posters
from ..tasks.putters import register_task_putters
from ..tasks.deleters import register_task_deleters


class TasksController:
    """Controller that aggregates task route groups.

    Attributes:
        router (APIRouter): Router for task endpoints.
        _project_manager (ProjectManager): Injected project manager.
    """

    def __init__(self, project_manager: ProjectManager) -> None:
        """Constructs TasksController with injected project manager."""
        self._project_manager: ProjectManager = project_manager
        self.router: APIRouter = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])
        self._register()

    def _register(self) -> None:
        """Registers grouped route handlers onto router."""
        register_task_getters(router=self.router, project_manager=self._project_manager)
        register_task_posters(router=self.router, project_manager=self._project_manager)
        register_task_putters(router=self.router, project_manager=self._project_manager)
        register_task_deleters(router=self.router, project_manager=self._project_manager)
