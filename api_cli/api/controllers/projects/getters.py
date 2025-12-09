from fastapi import APIRouter, HTTPException
from typing import List, Optional

from api_cli.api.schemas.responses.project_response_schema import ProjectResponse
from api_cli.api.schemas.detail_schema import DetailSchema
from service.project_manager import ProjectManager
from models.models import Project


def _find_project(manager: ProjectManager, project_id: int) -> Project:
    """Locate a project by id or raise 404."""
    projects = manager.get_repo_list()
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def register_project_getters(router: APIRouter, manager: ProjectManager) -> None:
    """Register GET endpoints for projects."""

    @router.get(
        "/",
        response_model=Optional[List[ProjectResponse]],
        responses={500: {"description": "Internal server error"}},
    )
    def get_projects():
        """Return all projects or None when empty.

        Returns:
            Optional[List[ProjectResponse]]: List of projects or None.
        Raises:
            HTTPException: 500 on unexpected errors.
        """
        try:
            projects = manager.get_repo_list()
            if not projects:
                return None
            return [
                ProjectResponse(id=p.id, detail=DetailSchema.from_detail(p.detail))
                for p in projects
            ]
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    @router.get(
        "/{project_id}",
        response_model=ProjectResponse,
        responses={404: {"description": "Project not found"},
                   500: {"description": "Internal server error"}},
    )
    def get_project(project_id: int):
        """Return a single project by id.

        Args:
            project_id (int): Identifier of the project.
        Returns:
            ProjectResponse: The requested project representation.
        Raises:
            HTTPException: 404 if not found, 500 on other errors.
        """
        try:
            project = _find_project(manager=manager, project_id=project_id)
            return ProjectResponse(id=project.id, detail=DetailSchema.from_detail(project.detail))
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
