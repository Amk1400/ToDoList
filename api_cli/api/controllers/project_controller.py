from fastapi import APIRouter, HTTPException
from typing import List, Optional

from api_cli.api.schemas.requests.project_request_schema import ProjectUpdate, ProjectCreate
from api_cli.api.schemas.responses.project_response_schema import ProjectResponse
from service.project_manager import ProjectManager
from models.models import Detail, Project
from api_cli.api.schemas.detail_schema import DetailSchema


class ProjectController:
    """Controller for managing projects."""

    def __init__(self, manager: ProjectManager) -> None:
        self._manager = manager
        self.router = APIRouter(prefix="/projects", tags=["projects"])
        self._register()

    def _get_project(self, project_id: int) -> Project:
        project = None
        for p in self._manager.get_repo_list():
            if p.id == project_id:
                project = p
        if not project:
            raise HTTPException(404, "Project not found")
        return project

    def _register(self) -> None:
        @self.router.get(
            "/",
            response_model=Optional[List[ProjectResponse]],
            responses={500: {"description": "Internal server error"}},
        )
        def get_projects():
            try:
                projects = self._manager.get_repo_list()
                if not projects:
                    return None
                for p in projects:
                    print(type(p.detail))
                return [ProjectResponse(id=p.id, detail=DetailSchema.from_detail(p.detail)) for p in projects]
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.get(
            "/{project_id}",
            response_model=ProjectResponse,
            responses={404: {"description": "Project not found"},
                       500: {"description": "Internal server error"}},
        )
        def get_project(project_id: int):
            project = self._get_project(project_id)
            return ProjectResponse(id=project.id, detail=DetailSchema.from_detail(project.detail))

        @self.router.post(
            "/",
            response_model=Project,
            responses={400: {"description": "Invalid input"},
                       500: {"description": "Internal server error"}},
        )
        def create_project(data: ProjectCreate):
            try:
                detail = Detail(data.detail.title, data.detail.description)
                self._manager.add_entity(detail)
                new_project = self._manager.get_repo_list()[-1]
                return ProjectResponse(id=new_project.id, detail=DetailSchema.from_detail(new_project.detail))
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.put(
            "/{project_id}",
            response_model=ProjectResponse,
            responses={400: {"description": "Invalid input"}, 404: {"description": "Project not found"},
                       500: {"description": "Internal server error"}},
        )
        def update_project(project_id: int, data: ProjectUpdate):
            old = self._get_project(project_id)

            try:
                detail = Detail(data.detail.title, data.detail.description)
                updated = self._manager.create_entity_object(detail)
                self._manager.update_entity_object(old, updated)
                return ProjectResponse(id=old.id, detail=DetailSchema.from_detail(old.detail))
            except ValueError as exc:
                raise HTTPException(400, str(exc))
            except Exception as exc:
                raise HTTPException(500, str(exc))

        @self.router.delete(
            "/{project_id}",
            responses={404: {"description": "Project not found"},
                       500: {"description": "Internal server error"}},
        )
        def delete_project(project_id: int):
            project = self._get_project(project_id)
            try:
                self._manager.remove_entity_object(project)
                return {"detail": "Project deleted successfully"}
            except Exception as exc:
                raise HTTPException(500, str(exc))
