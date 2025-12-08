from __future__ import annotations
import os
import warnings
from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI
from uvicorn import run

from core.config import AppConfig
from db.db_inmemory import InMemoryDatabase
from db.db_postgres import PostgresDatabase
from repository.project_repository import ProjectRepository
from repository.task_repository import TaskRepository
from service.project_manager import ProjectManager
from service.scheduler.task_closer import TaskCloser
from service.scheduler.task_scheduler import TaskScheduler
from api_cli.api.controllers.project_controller import ProjectController
from api_cli.api import TaskController


def load_config() -> AppConfig:
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


def create_database(config: AppConfig, use_alembic: bool = False) -> Any:
    if config.db_type.lower() == "postgres":
        url = (
            f"postgresql://{config.db_user}:{config.db_password}"
            f"@{config.db_host}:{config.db_port}/{config.db_name}"
        )
        return PostgresDatabase(url, use_alembic=use_alembic)
    return InMemoryDatabase()


def create_scheduler(db: Any) -> None:
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    closer = TaskCloser(project_repo=project_repo, task_repo=task_repo)
    scheduler = TaskScheduler(jobs=[closer])
    scheduler.start_background()


app = FastAPI(title="ToDoList API", version="1.0")


def main(use_cli: bool = False) -> None:
    config, db, manager = _initialize()

    if use_cli:
        _run_cli(config, db, manager)
    else:
        _run_api(manager)


def _initialize() -> (AppConfig, PostgresDatabase | InMemoryDatabase, ProjectManager):
    config = load_config()
    db = create_database(config, use_alembic=True)
    create_scheduler(db)
    manager = ProjectManager(config, db)
    return config, db, manager


def _run_cli(config: AppConfig, db: PostgresDatabase | InMemoryDatabase, manager: ProjectManager) -> None:
    from api_cli.gateway import ProjectGateway
    from api_cli.cli.menus import MainMenu
    gateway = ProjectGateway(manager, config, db)
    menu = MainMenu(gateway)
    menu.run()


def _run_api(manager: ProjectManager) -> None:
    warnings.warn("CLI mode is disabled. Use API only.", DeprecationWarning)
    project_controller = ProjectController(manager)
    task_controller = TaskController(manager)
    app.include_router(project_controller.router)
    app.include_router(task_controller.router)
    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main(use_cli=False)
