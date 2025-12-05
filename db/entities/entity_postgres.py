from abc import abstractmethod
from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session

from db.orm_models import ProjectORM
from models.models import Project

T = TypeVar("T")


def _apply_detail_update(new_entity, orm_obj):
    orm_obj.title = new_entity.detail.title
    orm_obj.description = new_entity.detail.description


def _apply_postgres_remove(container, entity, orm_obj, session):
    session.delete(orm_obj)
    session.commit()
    container.remove(entity)


def _update_in_memory_container(container, new_entity, old_entity):
    if old_entity.tasks:
        new_entity.tasks = old_entity.tasks
    for index, item in enumerate(container):
        if item.detail.title == old_entity.detail.title:
            container[index] = new_entity
            return
    raise ValueError(f"Entity '{old_entity.detail.title}' not found in container.")


class EntityPostgres(Generic[T]):
    """Base class for Postgres entities."""

    def add_entity(self, entity: T, container: List[T], session: Session, parent: Optional[Project] = None) -> None:
        proj_orm = self._fetch_parent_proj_orm(parent, session)
        self._apply_postgres_add(container, entity, session, proj_orm)

    def remove_entity(self, entity: T, container: List[T], session: Session, parent: Optional[Project] = None) -> None:
        proj_orm = self._fetch_parent_proj_orm(parent, session)
        orm_object = self._fetch_orm(entity, session, parent, proj_orm)
        _apply_postgres_remove(container, entity, orm_object, session)

    def update_entity(self, old_entity: T, new_entity: T, container: List[T], session: Session, parent: Optional[Project] = None) -> None:
        parent_proj_orm = self._fetch_parent_proj_orm(parent, session)
        old_entity_orm = self._fetch_orm(old_entity, session, parent, parent_proj_orm)
        self._apply_postgres_update(new_entity, old_entity_orm, session)
        _update_in_memory_container(container, new_entity, old_entity)

    def _apply_postgres_add(self, container, entity, session, parent_proj_orm: Optional[Type[ProjectORM]]):
        entity_orm = self._create_orm_object(entity, parent_proj_orm)
        session.add(entity_orm)
        session.commit()
        container.append(entity)

    def _apply_postgres_update(self, new_entity, old_entity_orm, session):
        self._apply_deadline_and_task_update(new_entity, old_entity_orm)
        _apply_detail_update(new_entity, old_entity_orm)
        session.commit()

    @abstractmethod
    def load_all(self, session: Session) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def _apply_deadline_and_task_update(self, new_entity, old_entity_orm):
        raise NotImplementedError

    @abstractmethod
    def _create_orm_object(self, entity, parent_proj_orm: Optional[ProjectORM]):
        raise NotImplementedError

    @abstractmethod
    def _fetch_orm(self, entity, session, parent: Optional[Project], proj_orm: Optional[ProjectORM]):
        raise NotImplementedError

    @abstractmethod
    def _fetch_parent_proj_orm(self, parent, session):
        return None