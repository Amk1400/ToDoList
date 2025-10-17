import os
from dotenv import load_dotenv
from managers import ProjectManager
from config import AppConfig
import menu_manager


if __name__ == "__main__":
    load_dotenv()

    config = AppConfig(
        max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10")),
        max_project_name_length = int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30")),
        max_project_description_length = int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150")),
        max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "10")),
        max_task_name_length = int(os.getenv("MAX_TASK_NAME_LENGTH", "30")),
        max_task_description_length = int(os.getenv("MAX_TASK_DESCRIPTION_LENGTH", "150")),
    )

    project_manager = ProjectManager(config)
    menu_manager.run_main_menu(project_manager)
