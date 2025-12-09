from fastapi import APIRouter, HTTPException

from api_cli.api.schemas.requests.project_request_schema import ProjectUpdate
from api_cli.api.schemas.responses.project_response_schema import ProjectResponse
from api_cli.api.schemas.detail_schema import DetailSchema
from service.project_manager import ProjectManager
from models.models import Detail, Project


def _find_project(manager: ProjectManager, project_id: int) -> Project:
    """Find a project or raise 404."""
    project = next((p for p in manager.get_repo_list() if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def register_project_putters(router: APIRouter, manager: ProjectManager) -> None:
    """Register PUT endpoint for updating projects."""

    @router.put(
        "/{project_id}",
        response_model=ProjectResponse,
        responses={400: {"description": "Invalid input"}, 404: {"description": "Project not found"},
                   500: {"description": "Internal server error"}},
    )
    def update_project(project_id: int, data: ProjectUpdate):
        """Update existing project detail.

        Args:
            project_id (int): Identifier of the project.
            data (ProjectUpdate): Update payload.
        Returns:
            ProjectResponse: Updated project representation.
        Raises:
            HTTPException: 400 for invalid input, 404 if not found, 500 otherwise.
        """
        old = _find_project(manager=manager, project_id=project_id)
        try:
            detail = Detail(title=data.detail.title, description=data.detail.description)
            updated = manager.create_entity_object(detail)
            manager.update_entity_object(old, updated)
            return ProjectResponse(id=old.id, detail=DetailSchema.from_detail(old.detail))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
