# Student Assignment Tracker — IT 545 Final Project

## What the project does

This is a small Python web API for keeping a list of university assignments. A student can add an assignment, see the list, replace it, change one field, or remove it. Each assignment has a title, a course, and a completion status. The list is stored in memory, so it resets when the server restarts.

## Requirements

Python 3.13 and `uv`. The project uses FastAPI, Pydantic, and an in-memory repository. Tests use pytest and httpx.

## Run the project

```bash
uv sync --extra dev
uv run python -m assignment_tracker.app
```

Visit http://localhost:8000/docs to try the API with Swagger UI.

## Test

```bash
uv run pytest -q
```

## Endpoints

| Method | URL | Purpose |
| --- | --- | --- |
| GET | `/health/` | Check the server |
| GET | `/v1/assignment/` | List assignments; optional `course` and `limit` query |
| POST | `/v1/assignment/` | Add an assignment |
| PUT | `/v1/assignment/{index}` | Replace an assignment |
| PATCH | `/v1/assignment/{index}` | Change selected fields |
| DELETE | `/v1/assignment/{index}` | Delete an assignment |

Example POST JSON body:

```json
{"title": "Complete Python exercise", "course": "IT 545", "completed": false}
```

Example PATCH JSON body:

```json
{"completed": true}
```

Indexes start at 0. Like the lecturer's example, deleting an assignment changes the indexes of the assignments after it. This is a learning project, not a production database API.

## Connection with the student guides

- **Test 1 guide:** `Assignment` is a class; `__init__` creates instance attributes, `complete` and `summary` are methods; functions have type hints; modules are imported by package name; `uv` manages dependencies and Git can track changes.
- **Final exam guide:** FastAPI handles HTTP methods and status codes; Pydantic DTOs validate JSON; `APIRouter` builds `/v1/assignment/`; `Depends` supplies an `ICRUD[Assignment]` repository; `GradedAssignment` uses inheritance, `super()`, and method overriding; `ICRUD` defines abstract methods; the in-memory adapter implements that interface.

## Folder responsibilities

- `src/assignment_tracker/domain/`: classes representing assignments.
- `src/assignment_tracker/interface/api/dtos.py`: HTTP input/output Pydantic models.
- `src/assignment_tracker/interface/api/routers/`: HTTP routes only.
- `src/assignment_tracker/interface/api/dependencies/`: connects the API to the repository.
- `src/assignment_tracker/infrastructure/repositories/`: abstract storage interface.
- `src/assignment_tracker/infrastructure/adapters/`: in-memory implementation.
- `src/assignment_tracker/app.py`: creates the FastAPI app and connects routers.
- `tests/`: automated checks.

## Git workflow

Run `git pull` before editing an existing shared repository, then `git status`, `git add .`, `git commit -m "Build assignment tracker"`, and `git push`. Only commit work you have actually done. `.venv/` is excluded from Git.

## Notes for demonstrating the project

Explain the difference between a class and an object, why `self` is needed, how `PUT` differs from `PATCH`, why a missing index gives 404, and why the router depends on `ICRUD` instead of `InMemoryAssignmentRepository`. Be prepared to modify one of the endpoints yourself.
