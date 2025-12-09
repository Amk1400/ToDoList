from fastapi import APIRouter, HTTPException
from typing import List, Optional

from api_cli.api.schemas.requests.task_request_schema import TaskCreate, TaskUpdate
from api_cli.api.schemas.responses.task_response_schema import TaskResponse
from models.models import Detail
from service.project_manager import ProjectManager
from service.task_manager import TaskManager
from api_cli.api.schemas.detail_schema import DetailSchema


class TaskController:
    """Controller for managing tasks."""

    def __init__(self, project_manager: ProjectManager) -> None:
        self._project_manager = project_manager
        self.router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])
        self._register()

    def _get_task_manager(self, project_id: int) -> TaskManager:
        projects = self._project_manager.get_repo_list()
        project = None
        for p in projects:
            if p.id == project_id:
                project = p
        if not project:
            raise HTTPException(404, "Project not found")
        return self._project_manager.get_task_manager(project)

    def _register(self) -> None:
        @self.router.get(
            "/",
            response_model=Optional[List[TaskResponse]],
            responses={404: {"description": "Project not found"},
                       500: {"description": "Internal server error"}},
        )
        def get_tasks(project_id: int):
            try:
                manager = self._get_task_manager(project_id)
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
                        closed_at=t.closed_at
                    )
                    for t in tasks
                ]
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.get(
            "/{task_id}",
            response_model=TaskResponse,
            responses={404: {"description": "Project or Task not found"},
                       500: {"description": "Internal server error"}},
        )
        def get_task(project_id: int, task_id: int):
            manager = self._get_task_manager(project_id)
            task = next((t for t in manager.get_repo_list() if t.id == task_id), None)
            if not task:
                raise HTTPException(404, "Task not found")
            return TaskResponse(
                id=task.id,
                project_id=manager.get_parent_project().id,
                detail=DetailSchema.from_detail(task.detail),
                status=task.status,
                deadline=task.deadline,
                closed_at=task.closed_at
            )

        @self.router.post(
            "/",
            response_model=TaskResponse,
            responses={400: {"description": "Invalid input"},
                       404: {"description": "Project not found"},
                       500: {"description": "Internal server error"}},
        )
        def create_task(project_id: int, data: TaskCreate):
            manager = self._get_task_manager(project_id)
            try:
                detail = Detail(data.detail.title,data.detail.description)
                manager.add_entity(detail, data.deadline, data.status)
                new_task = manager.get_repo_list()[-1]
                return TaskResponse(
                    id=new_task.id,
                    project_id=manager.get_parent_project().id,
                    detail=DetailSchema.from_detail(new_task.detail),
                    status=new_task.status,
                    deadline=new_task.deadline
                )
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.put(
            "/{task_id}",
            response_model=TaskResponse,
            responses={400: {"description": "Invalid input"},
                       404: {"description": "Project or Task not found"},
                       500: {"description": "Internal server error"}},
        )
        def update_task(project_id: int, task_id: int, data: TaskUpdate):
            manager = self._get_task_manager(project_id)
            old = next((t for t in manager.get_repo_list() if t.id == task_id), None)
            if not old:
                raise HTTPException(404, "Task not found")

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
                    closed_at=old.closed_at
                )
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except HTTPException:
                raise
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.delete(
            "/{task_id}",
            responses={404: {"description": "Project or Task not found"},
                       500: {"description": "Internal server error"}},
        )
        def delete_task(project_id: int, task_id: int):
            manager = self._get_task_manager(project_id)
            task = next((t for t in manager.get_repo_list() if t.id == task_id), None)
            if not task:
                raise HTTPException(404, "Task not found")
            try:
                manager.remove_entity_object(task)
                return {"detail": "Task deleted successfully"}
            except Exception as exc:
                raise HTTPException(500, str(exc))
