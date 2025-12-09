from abc import abstractmethod
from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session

from db.orm_models import ProjectORM, TaskORM
from models.models import Project, Task

T = TypeVar("T")


def _apply_detail_update(new_entity: T, orm_obj: Type[TaskORM | ProjectORM]) -> None:
    """Apply detail field updates from entity to ORM object.

    Args:
        new_entity (T): Updated domain entity.
        orm_obj (Type[TaskORM | ProjectORM]): Target ORM object.

    Returns:
        None: No value is returned.
    """
    orm_obj.title = new_entity.detail.title
    orm_obj.description = new_entity.detail.description


def _apply_postgres_remove(
    container: List[T],
    entity: T,
    orm_obj: Type[TaskORM | ProjectORM],
    session: Session,
) -> None:
    """Remove an ORM object and its entity from persistence and memory.

    Args:
        container (List[T]): In-memory entity container.
        entity (T): Domain entity to remove.
        orm_obj (Type[TaskORM | ProjectORM]): ORM object to delete.
        session (Session): Active database session.

    Returns:
        None: No value is returned.
    """
    session.delete(orm_obj)
    session.commit()
    container.remove(entity)


def _update_in_memory_container(container: List[T], new_entity: T, old_entity: T) -> None:
    """Replace an entity inside an in-memory container.

    Args:
        container (List[T]): In-memory entity list.
        new_entity (T): Updated domain entity.
        old_entity (T): Original domain entity.

    Returns:
        None: No value is returned.

    Raises:
        ValueError: If the entity does not exist in the container.
    """
    if hasattr(old_entity, "tasks"):
        new_entity.tasks = old_entity.tasks
    for index, item in enumerate(container):
        if item.detail.title == old_entity.detail.title:
            container[index] = new_entity
            return
    raise ValueError(f"Entity '{old_entity.detail.title}' not found in container.")


class EntityPostgres(Generic[T]):
    """Base persistence contract for Postgres-backed entities.

    Attributes:
        None
    """

    def add_entity(
        self,
        entity: T,
        container: List[T],
        session: Session,
        parent: Optional[Project] = None,
    ) -> None:
        """Persist a new entity to Postgres and memory.

        Args:
            entity (T): Domain entity to add.
            container (List[T]): In-memory entity list.
            session (Session): Active database session.
            parent (Optional[Project]): Optional parent project.

        Returns:
            None: No value is returned.
        """
        proj_orm = self._fetch_parent_proj_orm(parent, session)
        self._apply_postgres_add(container, entity, session, proj_orm)

    def remove_entity(
        self,
        entity: T,
        container: List[T],
        session: Session,
        parent: Optional[Project] = None,
    ) -> None:
        """Remove an entity from Postgres and memory.

        Args:
            entity (T): Domain entity to remove.
            container (List[T]): In-memory entity list.
            session (Session): Active database session.
            parent (Optional[Project]): Optional parent project.

        Returns:
            None: No value is returned.
        """
        proj_orm = self._fetch_parent_proj_orm(parent, session)
        orm_object = self._fetch_orm(entity, session, parent, proj_orm)
        _apply_postgres_remove(container, entity, orm_object, session)

    def update_entity(
        self,
        old_entity: T,
        new_entity: T,
        container: List[T],
        session: Session,
        parent: Optional[Project] = None,
    ) -> None:
        """Update an existing entity in Postgres and memory.

        Args:
            old_entity (T): Original domain entity.
            new_entity (T): Updated domain entity.
            container (List[T]): In-memory entity list.
            session (Session): Active database session.
            parent (Optional[Project]): Optional parent project.

        Returns:
            None: No value is returned.
        """
        parent_proj_orm = self._fetch_parent_proj_orm(parent, session)
        old_entity_orm = self._fetch_orm(old_entity, session, parent, parent_proj_orm)
        self._apply_postgres_update(new_entity, old_entity_orm, session)
        _update_in_memory_container(container, new_entity, old_entity)

    def _apply_postgres_add(
        self,
        container: List[T],
        entity: T,
        session: Session,
        parent_proj_orm: Optional[Type[ProjectORM]],
    ) -> None:
        """Insert a new ORM object into Postgres.

        Args:
            container (List[T]): In-memory entity list.
            entity (T): Domain entity to persist.
            session (Session): Active database session.
            parent_proj_orm (Optional[Type[ProjectORM]]): Parent project ORM.

        Returns:
            None: No value is returned.
        """
        entity_orm = self._create_orm_object(entity, parent_proj_orm)
        session.add(entity_orm)
        session.commit()
        container.append(entity)

    def _apply_postgres_update(
        self,
        new_entity: T,
        old_entity_orm: Type[TaskORM | ProjectORM],
        session: Session,
    ) -> None:
        """Apply updates to an existing ORM object.

        Args:
            new_entity (T): Updated domain entity.
            old_entity_orm (Type[TaskORM | ProjectORM]): Existing ORM object.
            session (Session): Active database session.

        Returns:
            None: No value is returned.
        """
        self._apply_deadline_and_task_update(new_entity, old_entity_orm)
        _apply_detail_update(new_entity, old_entity_orm)
        session.commit()

    @abstractmethod
    def load_all(self, session: Session) -> List[T]:
        """Load all entities from Postgres.

        Args:
            session (Session): Active database session.

        Returns:
            List[T]: Loaded domain entities.
        """
        raise NotImplementedError

    @abstractmethod
    def _apply_deadline_and_task_update(self, new_entity: Task, old_entity_orm: Type[TaskORM]) -> None:
        """Apply additional task-specific update logic.

        Args:
            new_entity (Task): Updated task entity.
            old_entity_orm (Type[TaskORM]): Corresponding ORM instance.

        Returns:
            None: No value is returned.
        """
        raise NotImplementedError

    @abstractmethod
    def _create_orm_object(
        self,
        entity: T,
        parent_proj_orm: Optional[ProjectORM],
    ) -> TaskORM | ProjectORM:
        """Create an ORM object from a domain entity.

        Args:
            entity (T): Domain entity.
            parent_proj_orm (Optional[ProjectORM]): Parent project ORM.

        Returns:
            TaskORM | ProjectORM: Newly created ORM instance.
        """
        raise NotImplementedError

    @abstractmethod
    def _fetch_orm(
        self,
        entity: T,
        session: Session,
        parent: Optional[Project],
        parent_orm: Optional[ProjectORM],
    ) -> Type[TaskORM | ProjectORM]:
        """Fetch an ORM object corresponding to the given entity.

        Args:
            entity (T): Domain entity.
            session (Session): Active database session.
            parent (Optional[Project]): Parent project entity.
            parent_orm (Optional[ProjectORM]): Parent ORM project.

        Returns:
            Type[TaskORM | ProjectORM]: Matching ORM instance.
        """
        raise NotImplementedError

    @abstractmethod
    def _fetch_parent_proj_orm(self, parent: Optional[Project], session: Session) -> ProjectORM | None:
        """Fetch the parent project ORM object if required.

        Args:
            parent (Optional[Project]): Parent project entity.
            session (Session): Active database session.

        Returns:
            ProjectORM | None: Parent ORM instance if available.
        """
        return None
