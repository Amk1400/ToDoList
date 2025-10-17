from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Application configuration limits for projects and tasks.

    Attributes:
        max_projects (int): Maximum number of allowed projects.
        max_project_name_length (int): Maximum character length for a project's title.
        max_project_description_length (int): Maximum character length for a project's description.
        max_tasks (int): Maximum number of allowed tasks per project.
        max_task_name_length (int): Maximum character length for a task's title.
        max_task_description_length (int): Maximum character length for a task's description.
    """
    max_projects: int
    max_project_name_length: int
    max_project_description_length: int
    max_tasks: int
    max_task_name_length: int
    max_task_description_length: int
