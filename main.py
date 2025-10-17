import os
from dotenv import load_dotenv
import menu_manager
from managers import ProjectManager


if __name__ == "__main__":
    load_dotenv()

    project_manager = ProjectManager(
        max_projects=int(os.getenv("MAX_NUMBER_OF_PROJECT", "10")),
        max_name_length=int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30")),
        max_description_length=int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150")),
        max_tasks=int(os.getenv("MAX_NUMBER_OF_TASK", "10")),
        max_task_name_length=int(os.getenv("MAX_TASK_NAME_LENGTH", "30")),
        max_task_description_length=int(os.getenv("MAX_TASK_DESCRIPTION_LENGTH", "150")),
    )

    menu_manager.run_main_menu(project_manager)
