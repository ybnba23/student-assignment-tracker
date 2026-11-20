from pydantic import BaseModel, Field


class AssignmentIn(BaseModel):
    title: str = Field(min_length=1)
    course: str = Field(min_length=1)
    completed: bool = False


class AssignmentPatch(BaseModel):
    title: str | None = None
    course: str | None = None
    completed: bool | None = None


class AssignmentOut(BaseModel):
    title: str
    course: str
    completed: bool


class DataResponse(BaseModel):
    data: list[AssignmentOut]


class HealthResponse(BaseModel):
    status: str
