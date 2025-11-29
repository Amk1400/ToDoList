# tests/test_project_creation.py
import pytest
from unittest.mock import patch
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


def test_create_project_with_valid_inputs(manager):
    """Test creating a project with valid inputs."""
    inputs = iter(["ValidTitle", "ValidDescription"])

    def mock_input(prompt):
        return next(inputs)

    with patch("builtins.input", mock_input):
        detail = Detail(title=mock_input("title"), description=mock_input("desc"))
        manager.add_entity(detail=detail)

    # Check project is created
    assert len(manager.get_repo_list()) == 1
    created_project = manager.get_repo_list()[0]
    assert created_project.detail.title == "ValidTitle"
    assert created_project.detail.description == "ValidDescription"


def test_create_project_with_empty_title(manager):
    """Empty title should trigger EmptyValueError."""
    with pytest.raises(EmptyValueError):
        manager.validate_title("")


def test_create_project_with_invalid_title_length(manager):
    """Title exceeding max length triggers MaxLengthError."""
    long_title = "A" * (manager._config.max_project_name_length + 1)
    with pytest.raises(MaxLengthError):
        manager.validate_title(long_title)


def test_create_project_with_duplicate_title(manager):
    """Duplicate title triggers DuplicateValueError."""
    existing_detail = Detail(title="DuplicateTitle", description="Desc")
    manager._entity_list.append(manager._create_entity_object(detail=existing_detail))

    with pytest.raises(DuplicateValueError):
        manager.validate_title("DuplicateTitle")


def test_create_project_with_empty_description(manager):
    """Empty description should trigger EmptyValueError."""
    with pytest.raises(EmptyValueError):
        manager.validate_description("")


def test_create_project_with_invalid_description_length(manager):
    """Description exceeding max length triggers MaxLengthError."""
    long_desc = "D" * (manager._config.max_project_description_length + 1)
    with pytest.raises(MaxLengthError):
        manager.validate_description(long_desc)
