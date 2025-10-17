import menu_manager
from managers import ProjectManager

if __name__ == "__main__":
    project_manager = ProjectManager()
    menu_manager.run_main_menu(project_manager)
