from managers import ProjectManager, Project


def run_main_menu(project_manager: ProjectManager) -> None:
    """Display and control the main menu."""
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
    """Display and control the project management menu."""
    while True:
        print("\n--- PROJECTS MENU ---")
        print("1. View All Projects")
        print("2. Add New Project")
        print("3. Rename Project")
        print("4. Delete Project")
        print("5. Manage Project Tasks")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            _display_projects(project_manager)
        elif choice == "2":
            _handle_add_project(project_manager)
        elif choice == "3":
            _handle_rename_project(project_manager)
        elif choice == "4":
            _handle_delete_project(project_manager)
        elif choice == "5":
            _handle_manage_tasks(project_manager)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


def _display_projects(project_manager: ProjectManager) -> None:
    """Show list of all projects."""
    projects = project_manager.get_all_projects()
    if not projects:
        print("No projects available.")
        return
    for idx, project in enumerate(projects, start=1):
        print(f"{idx}. {project.name}")
        print(f"   {project.description[:80]}...")


def _handle_add_project(project_manager: ProjectManager) -> None:
    """Add a new project through user input."""
    name = input("Enter project name: ").strip()
    description = input("Enter project description: ").strip()
    try:
        project_manager.create_project(name, description)
        print("Project created successfully.")
    except ValueError as e:
        print(f"Validation error: {e}")
    except OverflowError as e:
        print(f"Limit error: {e}")


def _handle_rename_project(project_manager: ProjectManager) -> None:
    """Rename a project through user input."""
    _display_projects(project_manager)
    if not project_manager.get_all_projects():
        return
    try:
        index = int(input("Enter project number to rename: ")) - 1
        new_name = input("Enter new project name: ").strip()
        project_manager.update_project_name(index, new_name)
        print("Project renamed successfully.")
    except ValueError as e:
        print(f"Validation error: {e}")
    except IndexError as e:
        print(f"Selection error: {e}")


def _handle_delete_project(project_manager: ProjectManager) -> None:
    """Delete a project through user input."""
    _display_projects(project_manager)
    if not project_manager.get_all_projects():
        return
    try:
        index = int(input("Enter project number to delete: ")) - 1
        project_manager.remove_project(index)
        print("Project deleted successfully.")
    except ValueError:
        print("Invalid input, please enter a number.")
    except IndexError as e:
        print(f"Selection error: {e}")


def _handle_manage_tasks(project_manager: ProjectManager) -> None:
    """Ask user to select a project for task management."""
    projects = project_manager.get_all_projects()
    if not projects:
        print("No projects available to manage tasks.")
        return

    print("\nSelect a project to manage its tasks:")
    _display_projects(project_manager)

    try:
        index = int(input("Enter project number: ")) - 1
        selected_project = projects[index]
        print(f"You selected: {selected_project.name}")
        _open_task_management_menu(selected_project)
    except ValueError:
        print("Invalid input, please enter a number.")
    except IndexError:
        print("Invalid project selection.")


def _open_task_management_menu(project: Project) -> None:
    """Open the task management menu for a specific project."""
    print(f"\n--- TASK MANAGEMENT for {project.name} ---")
    pass #it returns main menu
