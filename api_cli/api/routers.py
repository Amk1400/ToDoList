from fastapi import APIRouter
from service.project_manager import ProjectManager

from .controllers.projects.controller import ProjectsController
from .controllers.tasks.controller import TasksController


def get_api_router(manager: ProjectManager) -> APIRouter:
    """Return a central APIRouter with all project and task routers mounted.

    Args:
        manager (ProjectManager): Injected project manager.
    Returns:
        APIRouter: Combined API router.
    """
    router = APIRouter()

    # Create controllers
    projects_controller = ProjectsController(manager)
    tasks_controller = TasksController(manager)

    # Include their routers
    router.include_router(projects_controller.router)
    router.include_router(tasks_controller.router)

    return router
