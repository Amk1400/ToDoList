from fastapi import APIRouter

root_router = APIRouter()

# create shared ProjectManager instance if needed for router
# in your main.py we already inject managers; here is an example if needed standalone
# project_manager = ProjectManager(config, db)

# Example usage if needed standalone (replace with dependency injection in main)
# project_controller = ProjectController(project_manager)
# task_controller = TaskController(project_manager)
# root_router.include_router(project_controller.router)
# root_router.include_router(task_controller.router)