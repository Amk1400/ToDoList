import os
from dotenv import load_dotenv
import menu_manager
from managers import ProjectManager


if __name__ == "__main__":
    load_dotenv()

    max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
    max_name_len = int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30"))
    max_desc_len = int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150"))

    project_manager = ProjectManager(
        max_projects=max_projects,
        max_name_length=max_name_len,
        max_description_length=max_desc_len,
    )

    menu_manager.run_main_menu(project_manager)
