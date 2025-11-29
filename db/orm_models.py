from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ProjectORM(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    tasks = relationship("TaskORM", back_populates="project", cascade="all, delete-orphan")

class TaskORM(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    deadline = Column(Date, nullable=True)
    status = Column(String(20), nullable=True)

    project = relationship("ProjectORM", back_populates="tasks")
