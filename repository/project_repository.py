from typing import List, Optional

from models.models import Project
from repository.entity_repository import EntityRepository


class ProjectRepository(EntityRepository[Project]):
    """Repository for managing project entities."""
    """
    Attributes:
        _db: Database handler for project operations.
    """

    def get_db_list(self, parent_entity: Optional[Project] = None) -> List[Project]:
        """Retrieve all projects."""
        """
        Args:
            parent_entity (Optional[Project]): Unused.

        Returns:
            List[Project]: List of all projects.

        Raises:
            None
        """
        return self._db.get_projects()

    def append_to_db(self, entity: Project, parent_entity: Optional[Project] = None) -> None:
        """Store a project in the database."""
        """
        Args:
            entity (Project): Project to add.
            parent_entity (Optional[Project]): Unused.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._db.add_project(entity)

    def remove_from_db(self, entity: Project, parent_entity: Optional[Project] = None) -> None:
        """Remove a project from the database."""
        """
        Args:
            entity (Project): Project to remove.
            parent_entity (Optional[Project]): Unused.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._db.remove_project(entity)

    def update_entity(
        self,
        parent_project: Optional[Project],
        old_entity: Project,
        new_entity: Project,
    ) -> None:
        """Update an existing project."""
        """
        Args:
            parent_project (Optional[Project]): Unused.
            old_entity (Project): Original project.
            new_entity (Project): Updated project.

        Returns:
            None: No return value.

        Raises:
            None
        """
        self._db.update_entity(old_entity, new_entity, None)
