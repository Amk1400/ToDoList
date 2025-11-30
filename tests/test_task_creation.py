import pytest
from datetime import date, timedelta
from models.models import Detail
from service.project_manager import ProjectManager
from core.config import AppConfig
from exception.exceptions import (
    EmptyValueError,
    MaxLengthError,
    DuplicateValueError,
    InvalidStatusError,
    InvalidDateError,
)

@pytest.fixture
def manager():
    config = AppConfig(
        max_projects=10,
        max_project_name_length=30,
        max_project_description_length=150,
        max_tasks=3,
        max_task_name_length=30,
        max_task_description_length=150,
    )
    return ProjectManager(config)

@pytest.fixture
def project(manager):
    detail = Detail(title="Project1", description="Desc1")
    manager.add_entity(detail)
    proj = manager.get_repo_list()[0]
    tm = manager.get_task_manager()
    tm.set_parent_project(proj)
    return proj

def test_task_valid_creation(manager, project):
    tm = manager.get_task_manager()
    detail = Detail(title="Task1", description="Valid description")
    tm.validate_title(detail.title)
    tm.validate_description(detail.description)
    tm.validate_status("todo")
    tm.validate_deadline(date.today() + timedelta(days=1))

def test_task_empty_title_raises(manager, project):
    tm = manager.get_task_manager()
    with pytest.raises(EmptyValueError):
        tm.validate_title("")

def test_task_long_title_raises(manager, project):
    tm = manager.get_task_manager()
    long_title = "T" * (tm._config.max_task_name_length + 1)
    with pytest.raises(MaxLengthError):
        tm.validate_title(long_title)

def test_task_empty_description_raises(manager, project):
    tm = manager.get_task_manager()
    with pytest.raises(EmptyValueError):
        tm.validate_description("")

def test_task_long_description_raises(manager, project):
    tm = manager.get_task_manager()
    long_desc = "D" * (tm._config.max_task_description_length + 1)
    with pytest.raises(MaxLengthError):
        tm.validate_description(long_desc)

def test_task_invalid_status_raises(manager, project):
    tm = manager.get_task_manager()
    with pytest.raises(InvalidStatusError):
        tm.validate_status("invalid")

def test_task_empty_status_defaults_to_todo(manager, project):
    tm = manager.get_task_manager()
    status = tm.validate_status("")  # خالی باشه
    assert status is None  # وقتی خالیه، None برمی‌گرده و موقع ساخت Task ست میشه به todo

def test_task_invalid_deadline_raises(manager, project):
    tm = manager.get_task_manager()
    past_date = date.today() - timedelta(days=1)
    with pytest.raises(InvalidDateError):
        tm.validate_deadline(past_date)

def test_task_duplicate_title_raises(manager, project):
    tm = manager.get_task_manager()
    detail = Detail(title="Task1", description="Desc")
    tm.add_entity(detail, deadline=date.today() + timedelta(days=1))
    with pytest.raises(DuplicateValueError):
        tm.validate_title("Task1")
