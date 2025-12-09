from fastapi import APIRouter, HTTPException

from api_cli.api.schemas.requests.task_request_schema import TaskCreate
from api_cli.api.schemas.responses.task_response_schema import TaskResponse
from api_cli.api.schemas.detail_schema import DetailSchema
from models.models import Detail
from service.project_manager import ProjectManager


def _get_task_manager(project_manager: ProjectManager, project_id: int):
    """Return TaskManager for a project or raise 404."""
    projects = project_manager.get_repo_list()
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_manager.get_task_manager(project)


def register_task_posters(router: APIRouter, project_manager: ProjectManager) -> None:
    """Register POST endpoint for creating tasks."""

    @router.post(
        "/",
        response_model=TaskResponse,
        responses={400: {"description": "Invalid input"},
                   404: {"description": "Project not found"},
                   500: {"description": "Internal server error"}},
    )
    def create_task(project_id: int, data: TaskCreate):
        """Create a new task under a project.

        Args:
            project_id (int): Parent project identifier.
            data (TaskCreate): Task creation payload.
        Returns:
            TaskResponse: Created task representation.
        Raises:
            HTTPException: 400 for validation, 404 if project missing, 500 otherwise.
        """
        manager = _get_task_manager(project_manager, project_id)
        try:
            detail = Detail(title=data.detail.title, description=data.detail.description)
            manager.add_entity(detail, data.deadline, data.status)
            new_task = manager.get_repo_list()[-1]
            return TaskResponse(
                id=new_task.id,
                project_id=manager.get_parent_project().id,
                detail=DetailSchema.from_detail(new_task.detail),
                status=new_task.status,
                deadline=new_task.deadline,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
