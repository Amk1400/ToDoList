# tests/test_project_editing.py
import pytest
from models.models import Detail
from service.project_manager import ProjectManager
from core.config import AppConfig
from core.validator import EmptyValueError, MaxLengthError, DuplicateValueError


@pytest.fixture
def manager():
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
def existing_projects(manager):
    """Add two projects to manager for testing edit."""
    project1 = manager._create_entity_object(Detail(title="Project1", description="Desc1"))
    project2 = manager._create_entity_object(Detail(title="Project2", description="Desc2"))
    manager._entity_list.extend([project1, project2])
    return manager._entity_list


def test_edit_project_valid(manager, existing_projects):
    """Edit a project with valid new title and description."""
    project_to_edit = existing_projects[0]

    new_title = "NewProject1"
    new_description = "New Description"

    # Should pass without exceptions
    manager.validate_title(new_title, skip_current=project_to_edit.detail.title)
    manager.validate_description(new_description)

    # Apply edit
    project_to_edit.detail.title = new_title
    project_to_edit.detail.description = new_description

    # Verify changes
    assert project_to_edit.detail.title == new_title
    assert project_to_edit.detail.description == new_description


def test_edit_project_empty_title(manager, existing_projects):
    """Editing to empty title should raise EmptyValueError."""
    project_to_edit = existing_projects[0]
    with pytest.raises(EmptyValueError):
        manager.validate_title("", skip_current=project_to_edit.detail.title)


def test_edit_project_empty_description(manager, existing_projects):
    """Editing to empty description should raise EmptyValueError."""
    project_to_edit = existing_projects[0]
    with pytest.raises(EmptyValueError):
        manager.validate_description("")


def test_edit_project_title_too_long(manager, existing_projects):
    """Editing title beyond max length should raise MaxLengthError."""
    project_to_edit = existing_projects[0]
    long_title = "A" * (manager._config.max_project_name_length + 1)
    with pytest.raises(MaxLengthError):
        manager.validate_title(long_title, skip_current=project_to_edit.detail.title)


def test_edit_project_description_too_long(manager, existing_projects):
    """Editing description beyond max length should raise MaxLengthError."""
    project_to_edit = existing_projects[0]
    long_desc = "D" * (manager._config.max_project_description_length + 1)
    with pytest.raises(MaxLengthError):
        manager.validate_description(long_desc)


def test_edit_project_duplicate_title(manager, existing_projects):
    """Editing title to another existing project's title should raise DuplicateValueError."""
    project_to_edit = existing_projects[0]
    duplicate_title = existing_projects[1].detail.title
    with pytest.raises(DuplicateValueError):
        manager.validate_title(duplicate_title, skip_current=project_to_edit.detail.title)
