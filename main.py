import os
from dotenv import load_dotenv
import menu_manager
from managers import ProjectManager


if __name__ == "__main__":
    load_dotenv()
    max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
    project_manager = ProjectManager(max_projects=max_projects)
    menu_manager.run_main_menu(project_manager)
