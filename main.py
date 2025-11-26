import os
from dotenv import load_dotenv
from core.config import AppConfig
from service.project_manager import ProjectManager
from cli.main_menu import MainMenu
from cli.entity.gateway.project_gateway import ProjectGateway


def main() -> None:
    """Run the ToDo List application."""

    load_dotenv()
    config = _load_config()
    project_manager = ProjectManager(config)
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
