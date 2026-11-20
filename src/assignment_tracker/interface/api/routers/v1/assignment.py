from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from assignment_tracker.domain import Assignment
from assignment_tracker.infrastructure.repositories import ICRUD

from ...dependencies.repositories import get_assignment_repository
from ...dtos import AssignmentIn, AssignmentPatch, AssignmentOut, DataResponse

AssignmentRouter = APIRouter(prefix="/assignment", tags=["Assignments"])
AssignmentRepo = Annotated[ICRUD[Assignment], Depends(get_assignment_repository)]


def _not_found() -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, "Assignment not found")


def _to_response(repo: ICRUD[Assignment]) -> DataResponse:
    assignments = [
        AssignmentOut(title=a.title, course=a.course, completed=a.completed)
        for a in repo.list()
    ]
    return DataResponse(data=assignments)


@AssignmentRouter.get("/", summary="Get all assignments")
async def get_assignment(
    repo: AssignmentRepo,
    course: str | None = None,
    limit: int | None = None,
) -> DataResponse:
    assignments = repo.list()
    if course is not None:
        assignments = [a for a in assignments if course.lower() in a.course.lower()]
    if limit is not None:
        if limit < 0:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Limit cannot be negative")
        assignments = assignments[:limit]
    return DataResponse(data=[AssignmentOut(title=a.title, course=a.course, completed=a.completed) for a in assignments])


@AssignmentRouter.post("/", summary="Create an assignment", status_code=status.HTTP_201_CREATED)
async def post_assignment(assignment: AssignmentIn, repo: AssignmentRepo) -> DataResponse:
    try:
        repo.add(Assignment(assignment.title, assignment.course, assignment.completed))
    except ValueError as error:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(error)) from error
    return _to_response(repo)


@AssignmentRouter.put("/{index}", summary="Replace an assignment")
async def put_assignment(index: int, assignment: AssignmentIn, repo: AssignmentRepo) -> DataResponse:
    try:
        updated = Assignment(assignment.title, assignment.course, assignment.completed)
    except ValueError as error:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(error)) from error
    if not repo.replace(index, updated):
        raise _not_found()
    return _to_response(repo)


@AssignmentRouter.patch("/{index}", summary="Partially update an assignment")
async def patch_assignment(index: int, assignment: AssignmentPatch, repo: AssignmentRepo) -> DataResponse:
    assignments = repo.list()
    if not 0 <= index < len(assignments):
        raise _not_found()
    current = assignments[index]
    changes = assignment.model_dump(exclude_unset=True)
    if any(value is None for value in changes.values()):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Fields cannot be null")
    try:
        updated = Assignment(
            changes.get("title", current.title),
            changes.get("course", current.course),
            changes.get("completed", current.completed),
        )
    except ValueError as error:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(error)) from error
    repo.replace(index, updated)
    return _to_response(repo)


@AssignmentRouter.delete("/{index}", summary="Delete an assignment")
async def delete_assignment(index: int, repo: AssignmentRepo) -> DataResponse:
    if not repo.delete(index):
        raise _not_found()
    return _to_response(repo)
