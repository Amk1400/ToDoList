from fastapi import APIRouter, HTTPException

from api_cli.api.schemas.requests.task_request_schema import TaskUpdate
from api_cli.api.schemas.responses.task_response_schema import TaskResponse
from api_cli.api.schemas.detail_schema import DetailSchema
from service.project_manager import ProjectManager


def _get_task_manager(project_manager: ProjectManager, project_id: int):
    """Return TaskManager for a project or raise 404."""
    projects = project_manager.get_repo_list()
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_manager.get_task_manager(project)


def register_task_putters(router: APIRouter, project_manager: ProjectManager) -> None:
    """Register PUT endpoint for updating tasks."""

    @router.put(
        "/{task_id}",
        response_model=TaskResponse,
        responses={400: {"description": "Invalid input"},
                   404: {"description": "Project or Task not found"},
                   500: {"description": "Internal server error"}},
    )
    def update_task(project_id: int, task_id: int, data: TaskUpdate):
        """Update a task within a project.

        Args:
            project_id (int): Parent project identifier.
            task_id (int): Task identifier.
            data (TaskUpdate): Update payload.
        Returns:
            TaskResponse: Updated task representation.
        Raises:
            HTTPException: 400 for invalid input, 404 if missing, 500 otherwise.
        """
        manager = _get_task_manager(project_manager, project_id)
        old = next((t for t in manager.get_repo_list() if t.id == task_id), None)
        if not old:
            raise HTTPException(status_code=404, detail="Task not found")

        new_detail = data.detail if data.detail else old.detail
        new_deadline = data.deadline if data.deadline is not None else old.deadline
        new_status = data.status if data.status else old.status

        try:
            updated_task = manager.create_entity_object(new_detail, new_deadline, new_status)
            manager.update_entity_object(old, updated_task, manager.get_parent_project())
            return TaskResponse(
                id=updated_task.id,
                project_id=manager.get_parent_project().id,
                detail=DetailSchema.from_detail(updated_task.detail),
                status=updated_task.status,
                deadline=updated_task.deadline,
                closed_at=old.closed_at,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
