from fastapi import APIRouter, HTTPException

from service.project_manager import ProjectManager
from models.models import Project


def _find_project(manager: ProjectManager, project_id: int) -> Project:
    """Find a project or raise 404."""
    project = next((p for p in manager.get_repo_list() if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


def register_project_deleters(router: APIRouter, manager: ProjectManager) -> None:
    """Register DELETE endpoint for removing projects."""

    @router.delete(
        "/{project_id}",
        responses={404: {"description": "Project not found"},
                   500: {"description": "Internal server error"}},
    )
    def delete_project(project_id: int):
        """Delete a project by id.

        Args:
            project_id (int): Identifier of the project.
        Returns:
            dict: Deletion confirmation message.
        Raises:
            HTTPException: 404 if not found, 500 on other errors.
        """
        project = _find_project(manager=manager, project_id=project_id)
        try:
            manager.remove_entity_object(project)
            return {"detail": "Project deleted successfully"}
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
