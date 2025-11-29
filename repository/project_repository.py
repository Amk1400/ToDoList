from typing import List
from models.models import Project, Task
from repository.entity_repository import EntityRepository


class ProjectRepository(EntityRepository[Project]):
    """Repository for Project entities."""

    def get_db_list(self) -> List[Project]:
        """Return all projects in database."""
        return self._db.get_projects()

    def append_to_db(self, project: Project) -> None:
        """Add a project to database."""
        self._db.add_project(project)

    def remove_from_db(self, project: Project) -> None:
        """Remove a project from database."""
        self._db.remove_project(project)

