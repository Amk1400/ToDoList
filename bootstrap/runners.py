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
    """Runs CLI or API interfaces.

    Attributes:
        _api (FastAPI): FastAPI application instance.
    """

    def __init__(self) -> None:
        self._api: FastAPI = FastAPI(title="ToDoList API", version="1.0")

    @staticmethod
    def run_cli(config: AppConfig, db: Any, manager: ProjectManager) -> None:
        """Run the CLI interface.

        Args:
            config (AppConfig): Application configuration.
            db (Any): Database dependency object.
            manager (ProjectManager): Project manager service.

        Returns:
            None: No value is returned.

        Raises:
            Exception: If CLI execution fails.
        """
        gateway = ProjectGateway(manager=manager, config=config, db=db)
        menu = MainMenu(project_gateway=gateway)
        menu.run()

    def run_api(self, manager: ProjectManager) -> None:
        """Run the FastAPI server.

        Args:
            manager (ProjectManager): Project manager service.

        Returns:
            None: No value is returned.

        Raises:
            RuntimeError: If API startup fails.
        """
        warnings.warn("CLI mode is disabled. API mode only.", DeprecationWarning)

        api_router = get_api_router(manager)
        self._api.include_router(api_router)

        run(self._api, host="0.0.0.0", port=8000)
