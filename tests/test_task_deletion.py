# tests/test_task_deletion.py
from datetime import date, timedelta
import pytest
from unittest.mock import patch
from models.models import Detail, Project
from service.task_manager import TaskManager
from cli.gateway.task_gateway import TaskGateway
from cli.menus.entity.modify.task_modify import TaskModifyMenu


@pytest.fixture
def manager():
    from core.config import AppConfig
    config = AppConfig(
        max_projects=10,
        max_project_name_length=30,
        max_project_description_length=150,
        max_tasks=10,
        max_task_name_length=30,
        max_task_description_length=150,
    )
    return TaskManager(config=config)


@pytest.fixture
def project_with_tasks(manager):
    project = Project(detail=Detail(title="Project1", description="Desc1"))
    manager.set_current_project(project)

    # ایجاد یک تسک معتبر
    deadline = date.today() + timedelta(days=1)
    task_detail = Detail(title="Task1", description="TaskDesc")
    manager.add_entity(detail=task_detail, deadline=deadline, status="todo")
    return project


def test_delete_task_success(manager, project_with_tasks):
    """Deleting a task should remove it from project and manager."""
    task_manager = manager
    task = project_with_tasks.tasks[0]
    gateway = TaskGateway(manager=task_manager, project=project_with_tasks)
    menu = TaskModifyMenu(gateway=gateway, project=project_with_tasks, task=task)

    with patch("builtins.input", side_effect=["y"]), patch("builtins.print") as mock_print:
        menu.delete_entity()
        mock_print.assert_any_call(f"✅{task.detail.title} Deleted successfully.")

    assert task not in project_with_tasks.tasks
    assert task not in task_manager.get_repo_list()
