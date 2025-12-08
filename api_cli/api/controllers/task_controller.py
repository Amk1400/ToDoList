from __future__ import annotations
from typing import List
from fastapi import APIRouter, HTTPException
from service.task_manager import TaskManager
from service.project_manager import ProjectManager
from api_cli.api.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)
from models.models import Detail


class TaskController:
    def __init__(self, project_manager: ProjectManager) -> None:
        self._project_manager = project_manager
        self.router = APIRouter(
            prefix="/projects/{project_id}/tasks",
            tags=["tasks"],
        )
        self._register()

    def _get_task_manager(self, project_id: int) -> TaskManager:
        projects = self._project_manager.get_repo_list()
        project = next((p for p in projects if p._id == project_id), None)
        if not project:
            raise HTTPException(404, "Project not found")
        return self._project_manager.get_task_manager(project)

    def _register(self) -> None:
        @self.router.get("/", response_model=List[TaskResponse])
        def get_tasks(project_id: int):
            try:
                manager = self._get_task_manager(project_id)
                return manager.get_repo_list()
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.get("/{task_id}", response_model=TaskResponse)
        def get_task(project_id: int, task_id: int):
            manager = self._get_task_manager(project_id)
            tasks = manager.get_repo_list()
            task = next((t for t in tasks if t._id == task_id), None)
            if not task:
                raise HTTPException(404, "Task not found")
            return task

        @self.router.post("/", response_model=TaskResponse)
        def create_task(project_id: int, data: TaskCreate):
            manager = self._get_task_manager(project_id)

            try:
                manager.validate_creation()
                manager.validate_title(data.title)
                manager.validate_description(data.description)
                if data.deadline:
                    manager.validate_deadline(data.deadline)

                status = manager.validate_status(data.status)
                detail = Detail(data.title, data.description)

                manager.add_entity(detail, data.deadline, status)
                new_task = manager.get_repo_list()[-1]
                return TaskResponse.model_validate(new_task)
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.put("/{task_id}", response_model=TaskResponse)
        def update_task(project_id: int, task_id: int, data: TaskUpdate):
            manager = self._get_task_manager(project_id)
            tasks = manager.get_repo_list()

            old = next((t for t in tasks if t._id == task_id), None)
            if not old:
                raise HTTPException(404, "Task not found")

            new_title = data.title or old.detail.title
            new_desc = data.description or old.detail.description
            new_deadline = data.deadline if data.deadline is not None else old.deadline
            new_status_in = data.status or old.status

            try:
                manager.validate_title(new_title, skip_current=old.detail.title)
                manager.validate_description(new_desc)
                if new_deadline:
                    manager.validate_deadline(new_deadline)
                new_status = manager.validate_status(new_status_in)

                new_detail = Detail(new_title, new_desc)
                new_task = manager.create_entity_object(new_detail, new_deadline, new_status)

                manager.update_entity_object(old, new_task, manager.get_parent_project())

                return TaskResponse.model_validate(new_task)
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.delete("/{task_id}")
        def delete_task(project_id: int, task_id: int):
            manager = self._get_task_manager(project_id)

            task = next((t for t in manager.get_repo_list() if t._id == task_id), None)
            if not task:
                raise HTTPException(404, "Task not found")

            try:
                manager.remove_entity_object(task)
                return {"detail": "Task deleted successfully"}
            except Exception as exc:
                raise HTTPException(500, str(exc))