from menus.project_menu import ProjectMenu
from managers.project_manager import ProjectManager


class MainMenu:
    """Handles main menu interactions."""

    def __init__(self, project_manager: ProjectManager) -> None:
        """Initialize with dependency injection."""
        self._project_menu = ProjectMenu(project_manager)

    def run(self) -> None:
        """Run main menu loop."""
        while True:
            print("\n--- MAIN MENU ---")
            print("1. Manage Projects")
            print("2. Exit")

            choice = input("Choose an option: ").strip()
            if choice == "1":
                self._project_menu.run()
            elif choice == "2":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
