import os
from dotenv import load_dotenv
from core.config import AppConfig
from db.db import DataBase
from service.project_manager import ProjectManager
from service.task_manager import TaskManager
from cli.menus.main_menu import MainMenu
from cli.gateway.project_gateway import ProjectGateway


def main() -> None:
    """Run the ToDo List application."""

    load_dotenv()
    config = _load_config()

    # ایجاد یک instance دیتابیس مشترک
    db = DataBase()

    # ایجاد Repositoryها روی دیتابیس مشترک
    project_manager = ProjectManager(config, db)
    task_manager = TaskManager(config, db)

    # اتصال TaskManager به ProjectManager (cascade, set current project)
    project_manager.set_task_manager(task_manager)

    # Gateway و منو
    project_gateway = ProjectGateway(project_manager)
    main_menu = MainMenu(project_gateway)
    main_menu.run()


def _load_config() -> AppConfig:
    return AppConfig(
        max_projects=int(os.getenv("MAX_NUMBER_OF_PROJECT", "10")),
        max_project_name_length=int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30")),
        max_project_description_length=int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150")),
        max_tasks=int(os.getenv("MAX_NUMBER_OF_TASK", "10")),
        max_task_name_length=int(os.getenv("MAX_TASK_NAME_LENGTH", "30")),
        max_task_description_length=int(os.getenv("MAX_TASK_DESCRIPTION_LENGTH", "150")),
    )


if __name__ == "__main__":
    main()
