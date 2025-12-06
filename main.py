import os
from typing import Any
from dotenv import load_dotenv
from core.config import AppConfig
from db.db_inmemory import InMemoryDatabase
from db.db_postgres import PostgresDatabase
from db.session import DBSession
from service.project_manager import ProjectManager
from cli.gateway.project_gateway import ProjectGateway
from cli.menus.main_menu import MainMenu


class ApplicationInitializer:
    """Application initializer."""

    def __init__(self) -> None:
        self._config: AppConfig | None = None

    def load_config(self) -> AppConfig:
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

    def create_database(self, config: AppConfig, use_alembic: bool = False) -> Any:
        if config.db_type.lower() == "postgres":
            url = (
                f"postgresql://{config.db_user}:{config.db_password}"
                f"@{config.db_host}:{config.db_port}/{config.db_name}"
            )
            return PostgresDatabase(url, use_alembic=use_alembic)
        return InMemoryDatabase()

    def create_manager(self, config: AppConfig, db: Any) -> ProjectManager:
        return ProjectManager(config=config, db=db)

    def create_gateway(
        self,
        manager: ProjectManager,
        config: AppConfig,
        db: Any
    ) -> ProjectGateway:
        return ProjectGateway(manager=manager, config=config, db=db)

    def create_main_menu(self, gateway: ProjectGateway) -> MainMenu:
        return MainMenu(project_gateway=gateway)


def main() -> None:
    """Run application."""
    use_alembic = True

    initializer = ApplicationInitializer()
    config = initializer.load_config()
    db = initializer.create_database(config, use_alembic=use_alembic)
    manager = initializer.create_manager(config, db)
    gateway = initializer.create_gateway(manager, config, db)
    menu = initializer.create_main_menu(gateway)
    menu.run()


if __name__ == "__main__":
    main()
