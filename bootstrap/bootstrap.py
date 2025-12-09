from __future__ import annotations

import os
from typing import Tuple, Any
from dotenv import load_dotenv

from core.config import AppConfig
from db.db_inmemory import InMemoryDatabase
from db.db_postgres import PostgresDatabase
from repository.project_repository import ProjectRepository
from repository.task_repository import TaskRepository
from service.project_manager import ProjectManager
from service.scheduler.task_closer import TaskCloser
from service.scheduler.task_scheduler import TaskScheduler


class ApplicationBootstrap:
    """Handles application initialization.

    Attributes:
        None
    """

    def initialize(self) -> Tuple[AppConfig, Any, ProjectManager]:
        """Initialize configuration, database, scheduler, and manager.

        Returns:
            Tuple[AppConfig, Any, ProjectManager]: Configuration, database, and project manager instances.
        """
        config = self._load_config()
        db = self._create_database(config=config)
        self._create_scheduler(db=db)
        manager = ProjectManager(config=config, db=db)
        return config, db, manager

    @staticmethod
    def _load_config() -> AppConfig:
        """Load environment variables and build application configuration.

        Returns:
            AppConfig: Application configuration instance.
        """
        load_dotenv()
        return AppConfig(
            max_projects=int(os.getenv("MAX_NUMBER_OF_PROJECT", "10")),
            max_project_name_length=int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30")),
            max_project_description_length=int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150")),
            max_tasks=int(os.getenv("MAX_NUMBER_OF_TASK", "10")),
            max_task_name_length=int(os.getenv("MAX_TASK_NAME_LENGTH", "30")),
            max_task_description_length=int(os.getenv("MAX_TASK_DESCRIPTION_LENGTH", "150")),
            db_type=os.getenv("DB_TYPE", "memory"),
            db_name=os.getenv("DB_NAME", ""),
            db_user=os.getenv("DB_USER", ""),
            db_password=os.getenv("DB_PASSWORD", ""),
            db_host=os.getenv("DB_HOST", ""),
            db_port=int(os.getenv("DB_PORT", "5432")),
        )

    @staticmethod
    def _create_database(config: AppConfig) -> Any:
        """Create a database instance based on configuration.

        Args:
            config (AppConfig): Application configuration.

        Returns:
            Any: Initialized database instance.
        """
        if config.db_type.lower() == "postgres":
            url = (
                f"postgresql://{config.db_user}:{config.db_password}"
                f"@{config.db_host}:{config.db_port}/{config.db_name}"
            )
            return PostgresDatabase(url, use_alembic=True)
        return InMemoryDatabase()

    @staticmethod
    def _create_scheduler(db: Any) -> None:
        """Create and start the background task scheduler.

        Args:
            db (Any): Database dependency.

        Returns:
            None: No value is returned.
        """
        project_repo = ProjectRepository(db)
        task_repo = TaskRepository(db)
        closer = TaskCloser(project_repo=project_repo, task_repo=task_repo)
        scheduler = TaskScheduler(jobs=[closer])
        scheduler.start_background()
