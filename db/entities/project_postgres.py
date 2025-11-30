from typing import List
from sqlalchemy.orm import Session
from db.entities.entity_postgres import EntityPostgres
from db.orm_models import ProjectORM
from models.models import Project, Detail

class ProjectPostgres(EntityPostgres[Project]):

    def add_entity(self, entity: Project, container: List[Project], session: Session, parent=None) -> None:
        orm_obj = ProjectORM(title=entity.detail.title, description=entity.detail.description)
        session.add(orm_obj)
        session.commit()
        container.append(entity)

    def remove_entity(self, entity: Project, container: List[Project], session: Session, parent=None) -> None:
        orm_obj = session.query(ProjectORM).filter_by(title=entity.detail.title).one_or_none()
        if orm_obj is None:
            raise ValueError(f"Project '{entity.detail.title}' not found")
        session.delete(orm_obj)
        session.commit()
        container.remove(entity)

    def update_entity(self, old_entity: Project, new_entity: Project, container: List[Project], session: Session, parent=None) -> None:
        orm_obj = session.query(ProjectORM).filter_by(title=old_entity.detail.title).one_or_none()
        if orm_obj is None:
            raise ValueError(f"Project '{old_entity.detail.title}' not found")
        orm_obj.title = new_entity.detail.title
        orm_obj.description = new_entity.detail.description
        session.commit()
        proj_model = next(p for p in container if p.detail.title == old_entity.detail.title)
        proj_model.detail = new_entity.detail

    def load_all(self, session: Session) -> List[Project]:
        projects: List[Project] = []
        for obj in session.query(ProjectORM).all():
            tasks = [
                t for t in []  # تسک‌ها از TaskPostgres بارگذاری می‌شوند
            ]
            projects.append(Project(detail=Detail(obj.title, obj.description), tasks=tasks))
        return projects
