from fastapi import APIRouter, HTTPException
from typing import List, Optional

from api_cli.api.schemas.responses.task_response_schema import TaskResponse
from api_cli.api.schemas.detail_schema import DetailSchema
from service.project_manager import ProjectManager
from service.task_manager import TaskManager


def _get_task_manager(project_manager: ProjectManager, project_id: int) -> TaskManager:
    """Return TaskManager for a project or raise 404."""
    projects = project_manager.get_repo_list()
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_manager.get_task_manager(project)


def register_task_getters(router: APIRouter, project_manager: ProjectManager) -> None:
    """Register GET endpoints for tasks."""

    @router.get(
        "/",
        response_model=Optional[List[TaskResponse]],
        responses={404: {"description": "Project not found"},
                   500: {"description": "Internal server error"}},
    )
    def get_tasks(project_id: int):
        """Return all tasks for a project or None if empty.

        Args:
            project_id (int): Parent project identifier.
        Returns:
            Optional[List[TaskResponse]]: Tasks list or None.
        Raises:
            HTTPException: 404 if project missing, 500 on other errors.
        """
        try:
            manager = _get_task_manager(project_manager, project_id)
            tasks = manager.get_repo_list()
            if not tasks:
                return None
            return [
                TaskResponse(
                    id=t.id,
                    project_id=manager.get_parent_project().id,
                    detail=DetailSchema.from_detail(t.detail),
                    status=t.status,
                    deadline=t.deadline,
                    closed_at=t.closed_at,
                )
                for t in tasks
            ]
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    @router.get(
        "/{task_id}",
        response_model=TaskResponse,
        responses={404: {"description": "Project or Task not found"},
                   500: {"description": "Internal server error"}},
    )
    def get_task(project_id: int, task_id: int):
        """Return a single task by id within a project.

        Args:
            project_id (int): Parent project identifier.
            task_id (int): Task identifier.
        Returns:
            TaskResponse: The requested task representation.
        Raises:
            HTTPException: 404 if missing, 500 on other errors.
        """
        try:
            manager = _get_task_manager(project_manager, project_id)
            task = next((t for t in manager.get_repo_list() if t.id == task_id), None)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return TaskResponse(
                id=task.id,
                project_id=manager.get_parent_project().id,
                detail=DetailSchema.from_detail(task.detail),
                status=task.status,
                deadline=task.deadline,
                closed_at=task.closed_at,
            )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
