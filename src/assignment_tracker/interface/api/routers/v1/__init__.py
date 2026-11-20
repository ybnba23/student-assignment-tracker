from fastapi import APIRouter
from . import assignment

router = APIRouter(prefix="/v1")
router.include_router(assignment.AssignmentRouter)
