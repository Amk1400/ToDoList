from typing import List, Optional
from models.models import Project, Detail
from repository.entity_repository import EntityRepository

class ProjectRepository(EntityRepository[Project]):
    """Repository for Project entities."""

    def get_db_list(self, parent_entity: Optional[Project] = None) -> List[Project]:
        """Return all projects in database."""
        return self._db.get_projects()

    def append_to_db(self, entity: Project, parent_entity: Optional[Project] = None) -> None:
        """Add a project to database."""
        self._db.add_project(entity)

    def remove_from_db(self, entity: Project, parent_entity: Optional[Project] = None) -> None:
        """Remove a project from database."""
        self._db.remove_project(entity)

    def update_entity(self, parent_project: Optional[Project], old_entity: Project, new_entity: Project) -> None:
        """Update a project in the database."""
        self._db.update_entity(None, old_entity, new_entity)
