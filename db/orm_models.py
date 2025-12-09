from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class EntityORM(Base):
    """Abstract base for common ORM fields."""
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)


class ProjectORM(EntityORM):
    __tablename__ = "projects"
    tasks = relationship("TaskORM", back_populates="project", cascade="all, delete-orphan")


class TaskORM(EntityORM):
    __tablename__ = "tasks"
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    deadline = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=True)
    closed_at = Column(DateTime, nullable=True)
    project = relationship("ProjectORM", back_populates="tasks")
