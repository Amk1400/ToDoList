from managers import ProjectManager


def run_main_menu(project_manager: ProjectManager) -> None:
    """Display and control the main menu.

    Args:
        project_manager (ProjectManager): Injected project manager instance.

    Returns:
        None
    """
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
    """Display and control the project management menu.

    Args:
        project_manager (ProjectManager): Injected project manager instance.

    Returns:
        None
    """
    while True:
        print("\n--- PROJECTS MENU ---")
        print("1. View All Projects")
        print("2. Add New Project")
        print("3. Rename Project")
        print("4. Delete Project")
        print("5. Back to Main Menu")

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
            break
        else:
            print("Invalid choice. Please try again.")


def _display_projects(project_manager: ProjectManager) -> None:
    """Show list of all projects.

    Args:
        project_manager (ProjectManager): Manager instance.

    Returns:
        None
    """
    projects = project_manager.get_all_projects()
    if not projects:
        print("No projects available.")
        return
    for idx, project in enumerate(projects, start=1):
        print(f"{idx}. {project.name}")
        print(f"   {project.description[:80]}...")


def _handle_add_project(project_manager: ProjectManager) -> None:
    """Add a new project through user input.

    Args:
        project_manager (ProjectManager): Manager instance.

    Returns:
        None

    Raises:
        ValueError: If input validation fails.
        OverflowError: If project limit exceeded.
    """
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
    """Rename a project through user input.

    Args:
        project_manager (ProjectManager): Manager instance.

    Returns:
        None

    Raises:
        ValueError: If name invalid or not unique.
        IndexError: If invalid index provided.
    """
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
    """Delete a project through user input.

    Args:
        project_manager (ProjectManager): Manager instance.

    Returns:
        None

    Raises:
        IndexError: If invalid project index given.
    """
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
