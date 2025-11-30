from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = declarative_base()

class ProjectORM(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    tasks = relationship("TaskORM", back_populates="project", cascade="all, delete-orphan")


class TaskORM(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    deadline = Column(DateTime, nullable=True)
    status = Column(String(20), nullable=True)
    project = relationship("ProjectORM", back_populates="tasks")