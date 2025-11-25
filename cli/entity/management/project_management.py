from cli.entity.gateway.project_gateway import ProjectGateway
from cli.entity.management.entity_management import EntityManagementMenu
from cli.entity.show.project_show import ProjectShowMenu


class ProjectManagementMenu(EntityManagementMenu):
    """Menu for managing projects."""

    def _show_and_modify(self) -> None:
        ProjectShowMenu(self._manager, parent_menu=self).run()

    def _create_entity(self) -> None:
        try:
            ProjectGateway(self._manager).create_entity()
            print("✅ Project created successfully.")
        except Exception as e:
            self.handle_exception(e)
        self.run()


