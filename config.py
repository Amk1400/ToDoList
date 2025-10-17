from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Holds all configuration limits for projects and tasks."""
    max_projects: int
    max_project_name_length: int
    max_project_description_length: int
    max_tasks: int
    max_task_name_length: int
    max_task_description_length: int
