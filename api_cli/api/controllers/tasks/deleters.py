from fastapi import APIRouter, HTTPException

from service.project_manager import ProjectManager


def _get_task_manager(project_manager: ProjectManager, project_id: int):
    """Return TaskManager for a project or raise 404."""
    projects = project_manager.get_repo_list()
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_manager.get_task_manager(project)


def register_task_deleters(router: APIRouter, project_manager: ProjectManager) -> None:
    """Register DELETE endpoint for removing tasks."""

    @router.delete(
        "/{task_id}",
        responses={404: {"description": "Project or Task not found"},
                   500: {"description": "Internal server error"}},
    )
    def delete_task(project_id: int, task_id: int):
        """Delete a task by id within a project.

        Args:
            project_id (int): Parent project identifier.
            task_id (int): Task identifier.
        Returns:
            dict: Deletion confirmation message.
        Raises:
            HTTPException: 404 if missing, 500 otherwise.
        """
        manager = _get_task_manager(project_manager, project_id)
        task = next((t for t in manager.get_repo_list() if t.id == task_id), None)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        try:
            manager.remove_entity_object(task)
            return {"detail": "Task deleted successfully"}
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
