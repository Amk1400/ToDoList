import os
from dotenv import load_dotenv
from app.core.config import AppConfig
from app.services.project_service import ProjectManager
from app.cli.main_menu import MainMenu


def main() -> None:
    """Run the ToDo List application.

    Loads environment variables, initializes application configuration and
    dependencies, and starts the main menu loop.
    """
    load_dotenv()

    config = AppConfig(
        max_projects=int(os.getenv("MAX_NUMBER_OF_PROJECT", "10")),
        max_project_name_length=int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30")),
        max_project_description_length=int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150")),
        max_tasks=int(os.getenv("MAX_NUMBER_OF_TASK", "10")),
        max_task_name_length=int(os.getenv("MAX_TASK_NAME_LENGTH", "30")),
        max_task_description_length=int(os.getenv("MAX_TASK_DESCRIPTION_LENGTH", "150")),
    )

    project_manager: ProjectManager = ProjectManager(config)
    main_menu: MainMenu = MainMenu(project_manager)
    main_menu.run()


if __name__ == "__main__":
    main()
