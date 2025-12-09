from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()


class EntityORM(Base):
    """Base ORM with shared entity fields."""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    """Attributes:
        id (int): Primary key identifier.
        title (str): Unique title of the entity.
        description (str): Descriptive text for the entity.
    """


class ProjectORM(EntityORM):
    """ORM model representing a project."""

    __tablename__ = "projects"

    tasks = relationship(
        "TaskORM",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    """Attributes:
        tasks (list[TaskORM]): Collection of related tasks.
    """


class TaskORM(EntityORM):
    """ORM model representing a task."""

    __tablename__ = "tasks"

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    deadline = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=True)
    closed_at = Column(DateTime, nullable=True)

    project = relationship("ProjectORM", back_populates="tasks")

    """Attributes:
        project_id (int): Foreign key referencing parent project.
        deadline (DateTime): Task deadline timestamp.
        status (str): Current status of the task.
        closed_at (DateTime): Completion timestamp.
        project (ProjectORM): Linked parent project.
    """