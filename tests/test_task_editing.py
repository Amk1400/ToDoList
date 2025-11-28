import os

import pytest
from unittest.mock import patch
from datetime import date, timedelta
from cli.gateway.task_gateway import TaskGateway
from cli.menus.entity.modify.task_modify import TaskModifyMenu
from models.models import Project, Task, Detail
from core.config import AppConfig
from service.task_manager import TaskManager


@pytest.fixture
def setup_task_environment():
    config = AppConfig(
        max_projects=int(os.getenv("MAX_NUMBER_OF_PROJECT", "10")),
        max_project_name_length=int(os.getenv("MAX_PROJECT_NAME_LENGTH", "30")),
        max_project_description_length=int(os.getenv("MAX_PROJECT_DESCRIPTION_LENGTH", "150")),
        max_tasks=int(os.getenv("MAX_NUMBER_OF_TASK", "10")),
        max_task_name_length=int(os.getenv("MAX_TASK_NAME_LENGTH", "30")),
        max_task_description_length=int(os.getenv("MAX_TASK_DESCRIPTION_LENGTH", "150")),
    )
    manager = TaskManager(config=config)

    project = Project(detail=Detail(title="Project 1", description="Sample project"))
    task = Task(
        detail=Detail(title="Task 1", description="Sample task"),
        deadline=date.today() + timedelta(days=1),
        status="todo"
    )

    project.tasks.append(task)
    manager.set_current_project(project)
    gateway = TaskGateway(manager=manager, project=project)

    return gateway, project, task


def test_edit_task_title_retry(setup_task_environment):
    gateway, project, task = setup_task_environment
    modify_menu = TaskModifyMenu(gateway, project, task)

    def input_gen():
        yield ""  # empty title -> خطا
        yield "T" * 100  # too long title -> خطا
        yield "Valid Title"  # درست

    gen = input_gen()

    with patch('builtins.input', side_effect=lambda _: next(gen)), patch('builtins.print'):
        modify_menu._edit_entity()


def test_edit_task_description_retry(setup_task_environment):
    gateway, project, task = setup_task_environment
    modify_menu = TaskModifyMenu(gateway, project, task)

    def input_gen():
        yield task.detail.title
        yield ""  # empty -> خطا
        yield "D" * 200  # too long -> خطا
        yield "Valid Description"  # درست

    gen = input_gen()

    with patch('builtins.input', side_effect=lambda _: next(gen)), patch('builtins.print'):
        modify_menu._edit_entity()


def test_edit_task_deadline_retry(setup_task_environment):
    gateway, project, task = setup_task_environment
    modify_menu = TaskModifyMenu(gateway, project, task)

    invalid_deadline = str(date.today() - timedelta(days=5))  # گذشته -> خطا
    valid_deadline = date.today() + timedelta(days=5)  # درست

    def input_gen():
        yield task.detail.title
        yield task.detail.description
        yield invalid_deadline
        yield str(valid_deadline)
        yield task.status

    gen = input_gen()

    with patch('builtins.input', side_effect=lambda _: next(gen)), patch('builtins.print'):
        modify_menu._edit_entity()

    assert task.deadline == valid_deadline


def test_edit_task_status_retry(setup_task_environment):
    gateway, project, task = setup_task_environment
    modify_menu = TaskModifyMenu(gateway, project, task)

    def input_gen():
        yield task.detail.title
        yield task.detail.description
        yield str(task.deadline)
        yield "invalid_status"  # خطا
        yield "done"  # درست

    gen = input_gen()

    with patch('builtins.input', side_effect=lambda _: next(gen)), patch('builtins.print'):
        modify_menu._edit_entity()

    assert task.status == "done"
