from cli.entity.gateway.task_gateway import TaskGateway
from cli.entity.management.entity_management import EntityManagementMenu
from cli.entity.show.task_show import TaskShowMenu


class TaskManagementMenu(EntityManagementMenu):
    """Menu for managing tasks within a project."""

    def _show_and_modify(self) -> None:
        TaskShowMenu(self._manager, self._project, parent_menu=self).run()

    def _create_entity(self) -> None:
        try:
            TaskGateway(self._manager, self._project).create_entity()
            print("✅ Task created successfully.")
        except Exception as e:
            self.handle_exception(e)
        self.run()