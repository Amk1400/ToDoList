from managers.project_manager import ProjectManager
from models import Detail


def run_main_menu(project_manager: ProjectManager) -> None:
    """Run the main menu."""
    while True:
        print("\n--- MAIN MENU ---")
        print("1. View Projects")
        print("2. Create Project")
        print("3. Rename Project")
        print("4. Delete Project")
        print("5. Task Management")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            _view_projects(project_manager)
        elif choice == "2":
            _create_project(project_manager)
        elif choice == "3":
            _rename_project(project_manager)
        elif choice == "4":
            _delete_project(project_manager)
        elif choice == "5":
            _open_task_management_menu(project_manager)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")


def _view_projects(project_manager: ProjectManager) -> None:
    """View all projects."""
    projects = project_manager.get_all_projects()
    if not projects:
        print("No projects available.")
        return
    for i, p in enumerate(projects, start=1):
        print(f"{i}. {p.detail.title} - {p.detail.description}")


def _create_project(project_manager: ProjectManager) -> None:
    """Create a project."""
    title = input("Enter project title: ")
    description = input("Enter project description: ")
    try:
        project_manager.create_project(Detail(title=title, description=description))
        print("Project created successfully.")
    except Exception as e:
        print(f"Error: {e}")


def _rename_project(project_manager: ProjectManager) -> None:
    """Rename a project."""
    _view_projects(project_manager)
    try:
        index = int(input("Enter project number: ")) - 1
        new_name = input("Enter new title: ")
        project_manager.update_project_name(index, new_name)
        print("Project renamed successfully.")
    except Exception as e:
        print(f"Error: {e}")


def _delete_project(project_manager: ProjectManager) -> None:
    """Delete a project."""
    _view_projects(project_manager)
    try:
        index = int(input("Enter project number: ")) - 1
        project_manager.remove_project(index)
        print("Project deleted.")
    except Exception as e:
        print(f"Error: {e}")


def _open_task_management_menu(project_manager: ProjectManager) -> None:
    """Open the task management menu for a specific project."""
    projects = project_manager.get_all_projects()
    if not projects:
        print("No projects available.")
        return

    print("\nSelect a project to manage tasks:")
    for i, p in enumerate(projects, start=1):
        print(f"{i}. {p.detail.title}")

    try:
        project_index = int(input("Enter project number: ")) - 1
        project = projects[project_index]
        task_manager = project_manager.get_task_manager()
        _run_task_menu(task_manager, project)
    except Exception as e:
        print(f"Error: {e}")


def _run_task_menu(task_manager, project) -> None:
    """Manage tasks for a project."""
    while True:
        print(f"\n--- TASK MENU for {project.detail.title} ---")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Change Status")
        print("4. Delete Task")
        print("5. Back to Main Menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            _view_tasks(project)
        elif choice == "2":
            _add_task(task_manager, project)
        elif choice == "3":
            _change_status(task_manager, project)
        elif choice == "4":
            _delete_task(task_manager, project)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def _view_tasks(project) -> None:
    """View tasks in a project."""
    if not project.tasks:
        print("No tasks available.")
        return
    for i, t in enumerate(project.tasks, start=1):
        print(f"{i}. {t.detail.title} [{t.status}] - {t.detail.description}")


def _add_task(task_manager, project) -> None:
    """Add a new task."""
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    try:
        task_manager.add_task(project, Detail(title=title, description=description))
        print("Task added successfully.")
    except Exception as e:
        print(f"Error: {e}")


def _change_status(task_manager, project) -> None:
    """Change task status."""
    _view_tasks(project)
    try:
        index = int(input("Enter task number: ")) - 1
        new_status = input("Enter new status (todo/doing/done): ")
        task_manager.update_task_status(project, index, new_status)
        print("Task status updated.")
    except Exception as e:
        print(f"Error: {e}")


def _delete_task(task_manager, project) -> None:
    """Delete a task."""
    _view_tasks(project)
    try:
        index = int(input("Enter task number: ")) - 1
        task_manager.remove_task(project, index)
        print("Task deleted.")
    except Exception as e:
        print(f"Error: {e}")
