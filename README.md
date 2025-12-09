# ToDoList Application

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust, modular ToDoList application built with Python, supporting both CLI and API interfaces. It manages projects and tasks with validation, limits, and automated scheduling for closing overdue tasks. The application uses a clean architecture with repositories, services, and gateways for separation of concerns. It supports in-memory storage for quick prototyping and PostgreSQL for production-grade persistence, with Alembic for database migrations.

This project emphasizes maintainability, extensibility, and best practices like dependency injection, validation, and background scheduling. It's ideal for developers looking to study layered architectures or build upon a scalable task management system.

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI Mode](#cli-mode)
  - [API Mode](#api-mode)
- [Database Options](#database-options)
  - [In-Memory Database](#in-memory-database)
  - [PostgreSQL with Alembic](#postgresql-with-alembic)
- [Scheduling](#scheduling)
- [Validation and Limits](#validation-and-limits)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Project and Task Management**: Create, read, update, and delete (CRUD) projects and tasks with nested relationships (tasks belong to projects).
- **Validation Rules**: Ensures unique titles, non-empty values, length limits, valid statuses (todo, doing, done), and future deadlines.
- **Limits Enforcement**: Configurable maximums for number of projects/tasks, title/description lengths.
- **Automated Task Closure**: A background scheduler runs daily (at 21:55) to mark overdue tasks as "done" and set `closed_at`.
- **Dual Interfaces**:
  - **CLI**: Interactive menus for managing projects and tasks, with user-friendly prompts and error handling.
  - **API**: RESTful endpoints using FastAPI for programmatic access, with Pydantic schemas for request/response validation.
- **Database Flexibility**: Switch between in-memory (for development) and PostgreSQL (for persistence) via configuration.
- **Migrations with Alembic**: Automatic schema management for PostgreSQL, ensuring smooth database evolution.
- **Error Handling**: Custom exceptions for validation failures, duplicates, and limits.
- **Demo Data**: Pre-loaded sample projects and tasks for quick testing in both database modes.

## Architecture Overview

The application follows a layered architecture inspired by Clean Architecture:

- **Models**: Data classes for entities (Project, Task, Detail, Status).
- **Core**: Shared utilities like configuration and validators.
- **Database Layer**: Abstract interface with implementations for in-memory and PostgreSQL (using SQLAlchemy ORM).
- **Repository Layer**: Abstracts data access for projects and tasks.
- **Service Layer**: Business logic in managers (ProjectManager, TaskManager) and scheduler (TaskCloser, TaskScheduler).
- **API/CLI Layer**: Gateways and controllers/menus for user interaction, delegating to services.
- **Bootstrap**: Initializes config, DB, managers, and runners for CLI/API.

This separation ensures testability and easy extension (e.g., adding new databases or interfaces).

## Prerequisites

- Python 3.12+
- PostgreSQL (if using persistent DB; version 14+ recommended)
- Poetry (for dependency management)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/todolist-app.git
   cd todolist-app
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

   This sets up a virtual environment and installs all required packages (e.g., FastAPI, SQLAlchemy, Alembic, Schedule).

3. (Optional) Set up PostgreSQL:
   - Create a database (e.g., `todolist_db`).
   - Configure environment variables (see [Configuration](#configuration)).

4. Run Alembic migrations (for PostgreSQL):
   ```
   poetry run alembic upgrade head
   ```

## Configuration

The app loads config from `.env` (use `dotenv` for loading). Key variables:

- `MAX_NUMBER_OF_PROJECT`: Max projects (default: 10)
- `MAX_PROJECT_NAME_LENGTH`: Max project title length (default: 30)
- `MAX_PROJECT_DESCRIPTION_LENGTH`: Max project description length (default: 150)
- `MAX_NUMBER_OF_TASK`: Max tasks per project (default: 10)
- `MAX_TASK_NAME_LENGTH`: Max task title length (default: 30)
- `MAX_TASK_DESCRIPTION_LENGTH`: Max task description length (default: 150)
- `DB_TYPE`: "memory" or "postgres" (default: "memory")
- For PostgreSQL:
  - `DB_NAME`: Database name
  - `DB_USER`: Username
  - `DB_PASSWORD`: Password
  - `DB_HOST`: Host (default: localhost)
  - `DB_PORT`: Port (default: 5432)

Example `.env`:
```
DB_TYPE=postgres
DB_NAME=todolist_db
DB_USER=postgres
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5432
```

## Usage

### CLI Mode

Run the CLI:
```
poetry run python main.py --use-cli
```

- Navigate menus to manage projects/tasks.
- Inputs are validated interactively.
- Use "Back" to return to previous menus; "Exit" to quit.

### API Mode

Run the API server:
```
poetry run python main.py
```
Or directly with Uvicorn:
```
poetry run uvicorn bootstrap.runners:ApplicationRunners.run_api --reload
```

- Access at `http://localhost:8000`.
- Swagger docs: `http://localhost:8000/docs`.
- Endpoints:
  - **Projects**: GET/POST/PUT/DELETE `/projects/{project_id}`
  - **Tasks**: GET/POST/PUT/DELETE `/projects/{project_id}/tasks/{task_id}`

Example API request (create project):
```
curl -X POST "http://localhost:8000/projects/" -H "Content-Type: application/json" -d '{"detail": {"title": "New Project", "description": "Description"}}'
```

## Database Options

### In-Memory Database

- Default mode (`DB_TYPE=memory`).
- Data is volatile (lost on restart).
- Pre-loaded with demo data (2 projects, sample tasks).
- Ideal for development/testing.

### PostgreSQL with Alembic

- Set `DB_TYPE=postgres`.
- Uses SQLAlchemy ORM for CRUD.
- Alembic handles migrations: Run `alembic revision --autogenerate` for schema changes, then `alembic upgrade head`.
- Supports cascade deletes (tasks removed with projects).
- Demo data loaded on init if empty.

## Scheduling

- Uses `schedule` library for background task closure.
- Runs daily at 21:55 to update overdue tasks (`status=done`, set `closed_at`).
- Starts automatically on app bootstrap.
- No manual intervention needed; logs changes via repositories.

## Validation and Limits

- **Titles/Descriptions**: Non-empty, unique, max lengths enforced.
- **Statuses**: Only "todo", "doing", "done".
- **Deadlines**: YYYY-MM-DD, not in the past.
- **Counts**: Cannot exceed max projects/tasks.
- Errors raise custom exceptions with clear messages.

## Project Structure

```
todolist-app/
├── bootstrap/          # App initialization and runners
├── core/               # Shared config and validators
├── db/                 # Database interfaces, ORM, entities, sessions
│   ├── entities/       # Postgres-specific operations
│   └── orm_models.py   # SQLAlchemy models
├── exception/          # Custom exceptions
├── models/             # Data models (Project, Task, etc.)
├── repository/         # Data access abstractions
├── service/            # Business logic (managers, scheduler)
│   └── scheduler/      # Task closure and scheduling
├── tests/              # Unit/integration tests
├── api_cli/            # API and CLI implementations
│   ├── api/            # FastAPI routers, controllers, schemas
│   └── cli/            # Menus, fetchers, gateways
├── main.py             # Entry point
├── alembic/            # Migrations (if using Alembic)
├── poetry.lock         # Dependency lockfile
├── pyproject.toml      # Poetry config
└── README.md           # This file
```

## Dependencies

Managed via Poetry. Key packages:
- `fastapi`: API framework
- `uvicorn`: ASGI server
- `sqlalchemy`: ORM
- `psycopg2`: PostgreSQL driver
- `alembic`: Migrations
- `schedule`: Task scheduling
- `pydantic`: Schemas/validation
- `python-dotenv`: Env loading

View full list: `poetry show`.

## Testing

Run tests with Pytest:
```
poetry run pytest
```

- Covers validators, managers, repositories, and CLI/API interactions.
- Uses in-memory DB for isolation.

## Contributing

1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/xyz`).
3. Commit changes (`git commit -m "Add xyz"`).
4. Push (`git push origin feature/xyz`).
5. Open a Pull Request.

Follow Black code style and add tests for new features.

## License

MIT License. See [LICENSE](LICENSE) for details.