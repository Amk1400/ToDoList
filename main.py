from __future__ import annotations
import os
from typing import Any
from dotenv import load_dotenv
from core.config import AppConfig
from db.db_inmemory import InMemoryDatabase
from db.db_postgres import PostgresDatabase
from repository.project_repository import ProjectRepository
from repository.task_repository import TaskRepository
from service.project_manager import ProjectManager
from service.scheduler.task_closer import TaskCloser
from service.scheduler.task_scheduler import TaskScheduler
from cli.gateway.project_gateway import ProjectGateway
from cli.menus.main_menu import MainMenu


def create_database(config: AppConfig, use_alembic: bool = False) -> Any:
    """Create database backend."""
    if config.db_type.lower() == "postgres":
        url = (
            f"postgresql://{config.db_user}:{config.db_password}"
            f"@{config.db_host}:{config.db_port}/{config.db_name}"
        )
        return PostgresDatabase(url, use_alembic=use_alembic)
    return InMemoryDatabase()


def create_manager(config: AppConfig, db: Any) -> ProjectManager:
    """Create project manager."""
    return ProjectManager(config=config, db=db)


def create_gateway(manager: ProjectManager, config: AppConfig, db: Any) -> ProjectGateway:
    """Create project gateway."""
    return ProjectGateway(manager=manager, config=config, db=db)


def create_main_menu(gateway: ProjectGateway) -> MainMenu:
    """Create main menu."""
    return MainMenu(project_gateway=gateway)


def create_scheduler(db: Any) -> None:
    """Create task scheduler with TaskCloser jobs."""
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)

    closer = TaskCloser(project_repo=project_repo, task_repo=task_repo)
    scheduler = TaskScheduler(jobs=[closer])
    scheduler.start_background()


class ApplicationInitializer:
    """Initialize core components."""

    def __init__(self) -> None:
        self._config: AppConfig | None = None

    def load_config(self) -> AppConfig:
        """Load environment configuration."""
        load_dotenv()
        self._config = AppConfig(
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
        return self._config


def main() -> None:
    """Run the application."""
    initializer = ApplicationInitializer()
    config = initializer.load_config()

    db = create_database(config, use_alembic=True)
    manager = create_manager(config, db)
    gateway = create_gateway(manager, config, db)

    create_scheduler(db)
    _launch_cli(gateway)


def _launch_cli(gateway: ProjectGateway) -> None:
    menu = create_main_menu(gateway)
    menu.run()


if __name__ == "__main__":
    main()
