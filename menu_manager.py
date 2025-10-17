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
        _open_task_management_menu(selected_project, project_manager)
    except ValueError:
        print("Invalid input, please enter a number.")
    except IndexError:
        print("Invalid project selection.")


def _open_task_management_menu(project: Project, project_manager: ProjectManager) -> None:
    """Open the task management menu for a specific project."""
    while True:
        print(f"\n--- TASK MANAGEMENT for {project.name} ---")
        print("1. View All Tasks")
        print("2. Add Task")
        print("3. Change Task Status")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Back to Project Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            _display_tasks(project)
        elif choice == "2":
            _handle_add_task(project, project_manager)
        elif choice == "3":
            _handle_change_task_status(project)
        elif choice == "4":
            _handle_edit_task(project, project_manager)
        elif choice == "5":
            _handle_delete_task(project)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


def _display_tasks(project: Project) -> None:
    """Display all tasks for the selected project."""
    if not project.tasks:
        print("No tasks available for this project.")
        return
    for idx, task in enumerate(project.tasks, start=1):
        print(f"{idx}. {task.title} [{task.status}]")
        print(f"   {task.description[:80]}...")


def _handle_add_task(project: Project, project_manager: ProjectManager) -> None:
    """Handle adding a new task to the selected project."""
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    project_index = project_manager.get_all_projects().index(project)
    try:
        project_manager.add_task_to_project(project_index, title, description)
        print("Task added successfully.")
    except ValueError as e:
        print(f"Validation error: {e}")
    except OverflowError as e:
        print(f"Limit error: {e}")
    except IndexError as e:
        print(f"Selection error: {e}")


def _handle_change_task_status(project: Project) -> None:
    """Handle changing the status of a task."""
    _display_tasks(project)
    if not project.tasks:
        return
    try:
        index = int(input("Enter task number to change status: ")) - 1
        task = project.tasks[index]
        print("Choose new status:")
        print("1. todo")
        print("2. doing")
        print("3. done")
        status_choice = input("Enter choice: ").strip()
        status_map = {"1": "todo", "2": "doing", "3": "done"}
        if status_choice not in status_map:
            print("Invalid status choice.")
            return
        task.status = status_map[status_choice]
        print(f"Task '{task.title}' status updated to '{task.status}'.")
    except ValueError:
        print("Invalid input, please enter a number.")
    except IndexError:
        print("Invalid task selection.")


def _handle_edit_task(project: Project, project_manager: ProjectManager) -> None:
    """Handle editing an existing task."""
    _display_tasks(project)
    if not project.tasks:
        return
    try:
        task_index = int(input("Enter task number to edit: ")) - 1
        title = input("Enter new task title: ").strip()
        description = input("Enter new task description: ").strip()

        print("Choose new status:")
        print("1. todo")
        print("2. doing")
        print("3. done")
        status_choice = input("Enter choice: ").strip()
        status_map = {"1": "todo", "2": "doing", "3": "done"}

        if status_choice not in status_map:
            print("Invalid status choice.")
            return

        project_index = project_manager.get_all_projects().index(project)
        project_manager.update_task_details(
            project_index, task_index, title, description, status_map[status_choice]
        )
        print("Task updated successfully.")
    except ValueError as e:
        print(f"Validation error: {e}")
    except IndexError:
        print("Invalid task selection.")


def _handle_delete_task(project: Project) -> None:
    """Handle deleting a task from the selected project."""
    _display_tasks(project)
    if not project.tasks:
        return
    try:
        index = int(input("Enter task number to delete: ")) - 1
        del project.tasks[index]
        print("Task deleted successfully.")
    except ValueError:
        print("Invalid input, please enter a number.")
    except IndexError:
        print("Invalid task selection.")
