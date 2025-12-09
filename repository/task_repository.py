from typing import List, Optional

from models.models import Project, Task
from repository.entity_repository import EntityRepository


class TaskRepository(EntityRepository[Task]):
    """Repository for storing tasks within projects."""
    """
    Attributes:
        _db: Database handler for task operations.
    """

    def get_db_list(self, project: Optional[Project] = None) -> List[Task]:
        """Retrieve tasks of a project."""
        """
        Args:
            project (Optional[Project]): Project owning tasks.

        Returns:
            List[Task]: List of tasks for project.

        Raises:
            ValueError: If project is not provided.
        """
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        return self._db.get_tasks(project)

    def append_to_db(self, entity: Task, project: Optional[Project] = None) -> None:
        """Store a task in the given project."""
        """
        Args:
            entity (Task): Task to store.
            project (Optional[Project]): Associated project.

        Returns:
            None: No return value.

        Raises:
            ValueError: If project is not provided.
        """
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        self._db.add_task(project, entity)

    def remove_from_db(self, entity: Task, project: Optional[Project] = None) -> None:
        """Remove a task from a project."""
        """
        Args:
            entity (Task): Task to remove.
            project (Optional[Project]): Project owning the task.

        Returns:
            None: No return value.

        Raises:
            ValueError: If project is not provided.
        """
        if project is None:
            raise ValueError("Project must be provided for tasks.")
        self._db.remove_task(project, entity)

    def update_entity(
        self,
        parent_project: Optional[Project],
        old_entity: Task,
        new_entity: Task,
    ) -> None:
        """Update an existing task in a project."""
        """
        Args:
            parent_project (Optional[Project]): Project of task.
            old_entity (Task): Old task instance.
            new_entity (Task): Updated task instance.

        Returns:
            None: No return value.

        Raises:
            ValueError: If parent project is missing.
        """
        if parent_project is None:
            raise ValueError("Parent project must be provided for tasks.")
        self._db.update_entity(old_entity, new_entity, parent_project)
