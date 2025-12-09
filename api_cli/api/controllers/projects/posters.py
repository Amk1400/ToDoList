from fastapi import APIRouter, HTTPException

from api_cli.api.schemas.requests.project_request_schema import ProjectCreate
from api_cli.api.schemas.responses.project_response_schema import ProjectResponse
from api_cli.api.schemas.detail_schema import DetailSchema
from service.project_manager import ProjectManager
from models.models import Detail


def register_project_posters(router: APIRouter, manager: ProjectManager) -> None:
    """Register POST endpoint for creating projects."""

    @router.post(
        "/",
        response_model=ProjectResponse,
        responses={400: {"description": "Invalid input"},
                   500: {"description": "Internal server error"}},
    )
    def create_project(data: ProjectCreate):
        """Create a new project from provided detail.

        Args:
            data (ProjectCreate): Input payload for creation.
        Returns:
            ProjectResponse: Created project representation.
        Raises:
            HTTPException: 400 for validation, 500 for other errors.
        """
        try:
            detail = Detail(title=data.detail.title, description=data.detail.description)
            manager.add_entity(detail)
            new_project = manager.get_repo_list()[-1]
            return ProjectResponse(id=new_project.id, detail=DetailSchema.from_detail(new_project.detail))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
