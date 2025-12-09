from __future__ import annotations
from typing import Any
import warnings
from fastapi import FastAPI
from uvicorn import run

from api_cli.api.routers import get_api_router
from core.config import AppConfig
from service.project_manager import ProjectManager
from api_cli.gateway.project_gateway import ProjectGateway
from api_cli.cli.menus.main_menu import MainMenu


class ApplicationRunners:
    """Runs CLI or API interfaces."""

    def __init__(self) -> None:
        self._api: FastAPI = FastAPI(title="ToDoList API", version="1.0")

    @staticmethod
    def run_cli(config: AppConfig, db: Any, manager: ProjectManager) -> None:
        """Runs the CLI interface."""
        gateway = ProjectGateway(manager=manager, config=config, db=db)
        menu = MainMenu(project_gateway=gateway)
        menu.run()

    def run_api(self, manager: ProjectManager) -> None:
        """Runs the API server with all modular routers."""
        warnings.warn("CLI mode is disabled. API mode only.", DeprecationWarning)

        # Use central router instead of including controllers manually
        api_router = get_api_router(manager)
        self._api.include_router(api_router)

        run(self._api, host="0.0.0.0", port=8000)
