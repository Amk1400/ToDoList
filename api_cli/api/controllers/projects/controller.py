from fastapi import APIRouter
from service.project_manager import ProjectManager

from ..projects.getters import register_project_getters
from ..projects.posters import register_project_posters
from ..projects.putters import register_project_putters
from ..projects.deleters import register_project_deleters


class ProjectsController:
    """Controller that aggregates project route groups.

    Attributes:
        router (APIRouter): Router for project endpoints.
        _manager (ProjectManager): Injected project manager.
    """

    def __init__(self, manager: ProjectManager) -> None:
        """Constructs ProjectsController with injected manager."""
        self._manager: ProjectManager = manager
        self.router: APIRouter = APIRouter(prefix="/projects", tags=["projects"])
        self._register()

    def _register(self) -> None:
        """Registers grouped route handlers onto router."""
        register_project_getters(router=self.router, manager=self._manager)
        register_project_posters(router=self.router, manager=self._manager)
        register_project_putters(router=self.router, manager=self._manager)
        register_project_deleters(router=self.router, manager=self._manager)
