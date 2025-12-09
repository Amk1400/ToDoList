from __future__ import annotations
from typing import Any
import warnings
from fastapi import FastAPI
from uvicorn import run
from api_cli.gateway.project_gateway import ProjectGateway
from api_cli.cli.menus.main_menu import MainMenu
from api_cli.api.controllers.projects.controller import ProjectController
from api_cli.api.controllers.tasks.controller import TaskController
from core.config import AppConfig
from service.project_manager import ProjectManager


class ApplicationRunners:
    """Runs CLI or API interfaces."""

    def __init__(self) -> None:
        self._api = FastAPI(title="ToDoList API", version="1.0")

    @staticmethod
    def run_cli(config: AppConfig, db: Any, manager: ProjectManager) -> None:
        """Runs the CLI interface."""
        gateway = ProjectGateway(manager=manager, config=config, db=db)
        menu = MainMenu(project_gateway=gateway)
        menu.run()

    def run_api(self, manager: ProjectManager) -> None:
        """Runs the API server."""
        warnings.warn("CLI mode is disabled. API mode only.", DeprecationWarning)
        project_controller = ProjectController(manager=manager)
        task_controller = TaskController(project_manager=manager)
        self._api.include_router(project_controller.router)
        self._api.include_router(task_controller.router)
        run(self._api, host="0.0.0.0", port=8000)
