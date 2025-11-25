from cli.entity.gateway.entity_gateway import EntityGateway
from models.models import Project, Detail

class ProjectGateway(EntityGateway):
    """Gateway for fetching project inputs from CLI to Service."""

    def _create_fetch_optional(self) -> dict:
        """No optional fields for project creation."""
        return {}

    def edit_fetch_optional(self, entity: Project) -> dict:
        """No optional fields for project edition."""
        return {}

    def _apply_create(self, detail: Detail, optional_args: dict) -> None:
        """Create project using service manager."""
        self._manager.create_project(detail)

    def _apply_edit(self, entity: Project, detail: Detail, optional_args: dict) -> None:
        """Edit project using service manager."""
        # Find index of project in manager list
        projects = self._manager.get_all_projects()
        try:
            idx = projects.index(entity)
        except ValueError:
            print("Project not found.")
            return
        self._manager.update_project(idx, detail)
