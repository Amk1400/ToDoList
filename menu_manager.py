from managers import ProjectManager


def run_main_menu(project_manager: ProjectManager) -> None:
    """Handle main menu navigation."""
    while True:
        print("\n--- MAIN MENU ---")
        print("1. Manage Projects")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            show_projects_menu(project_manager)
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def show_projects_menu(project_manager: ProjectManager) -> None:
    """Handle project management menu navigation."""
    while True:
        print("\n--- PROJECTS MENU ---")
        print("1. View All Projects")
        print("2. Add New Project")
        print("3. Rename Project")
        print("4. Delete Project")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                _display_projects(project_manager)
            elif choice == "2":
                _handle_add_project(project_manager)
            elif choice == "3":
                _handle_rename_project(project_manager)
            elif choice == "4":
                _handle_delete_project(project_manager)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")


def _display_projects(project_manager: ProjectManager) -> None:
    """Display all projects to user."""
    projects = project_manager.get_all_projects()
    if not projects:
        print("No projects available. You can add one, by choosing option 2")
    else:
        for idx, name in enumerate(projects, start=1):
            print(f"{idx}. {name}")


def _handle_add_project(project_manager: ProjectManager) -> None:
    """Add new project via user input."""
    pass


def _handle_rename_project(project_manager: ProjectManager) -> None:
    """Rename project via user input."""
    _display_projects(project_manager)
    if not project_manager.get_all_projects():
        return
    try:
        index = int(input("Enter project number to rename: ")) - 1
        new_name = input("Enter new name: ").strip()
        project_manager.update_project_name(index, new_name)
        print("Project renamed successfully.")
    except ValueError:
        print("Invalid input, please enter a number.")


def _handle_delete_project(project_manager: ProjectManager) -> None:
    """Delete project via user input."""
    _display_projects(project_manager)
    if not project_manager.get_all_projects():
        return
    try:
        index = int(input("Enter project number to delete: ")) - 1
        project_manager.remove_project(index)
        print("Project deleted successfully.")
    except ValueError:
        print("Invalid input, please enter a number.")
