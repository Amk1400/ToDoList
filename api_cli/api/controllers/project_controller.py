from __future__ import annotations
from typing import List
from fastapi import APIRouter, HTTPException
from service.project_manager import ProjectManager
from api_cli.api.schemas.project_schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)
from models.models import Detail


class ProjectController:
    def __init__(self, manager: ProjectManager) -> None:
        self._manager = manager
        self.router = APIRouter(prefix="/projects", tags=["projects"])
        self._register()

    def _get_project(self, project_id: int):
        projects = self._manager.get_repo_list()
        return next((p for p in projects if p._id == project_id), None)

    def _register(self) -> None:
        @self.router.get("/", response_model=List[ProjectResponse])
        def get_projects():
            try:
                return self._manager.get_repo_list()
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.get("/{project_id}", response_model=ProjectResponse)
        def get_project(project_id: int):
            project = self._get_project(project_id)
            if not project:
                raise HTTPException(404, "Project not found")
            return project

        @self.router.post("/", response_model=ProjectResponse)
        def create_project(data: ProjectCreate):
            try:
                self._manager.validate_creation()
                self._manager.validate_title(data.title)
                self._manager.validate_description(data.description)

                detail = Detail(data.title, data.description)
                self._manager.add_entity(detail)
                new_project = self._manager.get_repo_list()[-1]
                return ProjectResponse.model_validate(new_project)
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.put("/{project_id}", response_model=ProjectResponse)
        def update_project(project_id: int, data: ProjectUpdate):
            old = self._get_project(project_id)
            if not old:
                raise HTTPException(404, "Project not found")

            new_title = data.title or old.detail.title
            new_desc = data.description or old.detail.description

            try:
                self._manager.validate_title(new_title, skip_current=old.detail.title)
                self._manager.validate_description(new_desc)

                detail = Detail(new_title, new_desc)
                updated = self._manager.create_entity_object(detail)
                self._manager.update_entity_object(old, updated)

                return ProjectResponse.model_validate(updated)
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.delete("/{project_id}")
        def delete_project(project_id: int):
            project = self._get_project(project_id)
            if not project:
                raise HTTPException(404, "Project not found")

            try:
                self._manager.remove_entity_object(project)
                return {"detail": "Project deleted successfully"}
            except Exception as exc:
                raise HTTPException(500, str(exc))