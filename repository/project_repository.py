from typing import List
from models.models import Project
from repository.entity_repository import EntityRepository

class ProjectRepository(EntityRepository[Project]):
    """Repository for Project entities."""

    def get_db_list(self, parent_entity: object | None = None) -> List[Project]:
        """Return all projects in database."""
        return self._db.get_projects()

    def append_to_db(self, entity: Project, parent_entity: object | None = None) -> None:
        """Add a project to database."""
        self._db.add_project(entity)

    def remove_from_db(self, entity: Project, parent_entity: object | None = None) -> None:
        """Remove a project from database."""
        self._db.remove_project(entity)