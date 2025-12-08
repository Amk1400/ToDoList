# tests/test_project_deletion.py
from datetime import timedelta, date

import pytest
from unittest.mock import patch

from cli.menus.entity.modify.project_modify import ProjectModifyMenu
from models.models import Detail
from service.project_manager import ProjectManager
from cli.gateway.project_gateway import ProjectGateway


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
    return ProjectManager(config)



@pytest.fixture
def project_with_tasks(manager):
    detail = Detail(title="Project1", description="Desc1")
    manager.add_entity(detail=detail)
    project = manager.get_repo_list()[0]

    task_manager = manager.get_task_manager()
    task_manager.set_parent_project(project)

    # ساخت یک تسک با deadline معتبر (مثلا فردا)
    deadline = date.today() + timedelta(days=1)
    task_detail = Detail(title="Task1", description="TaskDesc")
    task_manager.add_entity(detail=task_detail, deadline=deadline, status="todo")

    return project


@pytest.fixture
def project_without_tasks(manager):
    detail = Detail(title="Project2", description="Desc2")
    manager.add_entity(detail=detail)
    project = manager.get_repo_list()[0]
    return project


def test_delete_project_cascade(manager, project_with_tasks):
    """Deleting a project should remove it and its tasks from managers."""
    gateway = ProjectGateway(manager)
    task_manager = manager.get_task_manager()

    # Ensure project and task exist
    assert project_with_tasks in manager.get_repo_list()
    assert project_with_tasks.tasks[0] in task_manager.get_repo_list()

    menu = ProjectModifyMenu(gateway=gateway, project=project_with_tasks)

    # Delete project and check success message
    with patch("builtins.print") as mock_print:
        menu.delete_entity()
        mock_print.assert_any_call(f"✅{project_with_tasks.detail.title} Deleted successfully.")

    # Project should no longer exist
    assert project_with_tasks not in manager.get_repo_list()
    # Tasks should be removed from TaskManager
    for task in project_with_tasks.tasks:
        assert task not in task_manager.get_repo_list()


def test_delete_project_without_tasks(manager, project_without_tasks):
    """Deleting a project with no tasks should succeed."""
    gateway = ProjectGateway(manager)
    menu = ProjectModifyMenu(gateway=gateway, project=project_without_tasks)

    with patch("builtins.print") as mock_print:
        menu.delete_entity()
        mock_print.assert_any_call(f"✅{project_without_tasks.detail.title} Deleted successfully.")

    assert project_without_tasks not in manager.get_repo_list()
