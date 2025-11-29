import os
from dotenv import load_dotenv
from core.config import AppConfig
from db.db_inmemory import InMemoryDatabase
from db.db_postgres import PostgresDatabase
from service.project_manager import ProjectManager
from cli.menus.main_menu import MainMenu
from cli.gateway.project_gateway import ProjectGateway
from typing import Any


class ApplicationInitializer:
    """Initializes application components."""

    def __init__(self) -> None:
        self._config: AppConfig | None = None

    def load_config(self) -> AppConfig:
        """Load configuration from environment variables."""
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
            db_port=int(os.getenv("DB_PORT", "0")),
        )
        return self._config

    def create_database(self, config: AppConfig) -> Any:
        """Create database instance based on configuration."""
        if config.db_type.lower() == "postgres":
            return PostgresDatabase(
                db_name=config.db_name,
                user=config.db_user,
                password=config.db_password,
                host=config.db_host,
                port=config.db_port,
            )
        return InMemoryDatabase()

    def create_project_manager(self, config: AppConfig, db: Any) -> ProjectManager:
        """Create project manager instance."""
        return ProjectManager(config, db)

    def create_gateway(self, manager: ProjectManager, config: AppConfig, db: Any) -> ProjectGateway:
        """Create project gateway."""
        return ProjectGateway(manager, config, db)

    def create_main_menu(self, gateway: ProjectGateway) -> MainMenu:
        """Create main menu instance."""
        return MainMenu(gateway)


def main() -> None:
    """Run the ToDoList application."""
    initializer = ApplicationInitializer()
    config = initializer.load_config()
    db = initializer.create_database(config)
    project_manager = initializer.create_project_manager(config, db)
    gateway = initializer.create_gateway(project_manager, config, db)
    menu = initializer.create_main_menu(gateway)

    menu.run()


if __name__ == "__main__":
    main()
