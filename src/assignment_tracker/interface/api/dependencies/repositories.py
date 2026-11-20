from assignment_tracker.domain import Assignment
from assignment_tracker.infrastructure.adapters.in_memory_assignment_repository import InMemoryAssignmentRepository
from assignment_tracker.infrastructure.repositories import ICRUD

assignment_repository: ICRUD[Assignment] = InMemoryAssignmentRepository()


def get_assignment_repository() -> ICRUD[Assignment]:
    return assignment_repository
