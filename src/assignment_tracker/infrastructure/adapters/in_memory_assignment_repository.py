from assignment_tracker.domain import Assignment
from assignment_tracker.infrastructure.repositories import ICRUD


class InMemoryAssignmentRepository(ICRUD[Assignment]):
    def __init__(self, assignments: list[Assignment] | None = None) -> None:
        self._assignments = assignments if assignments is not None else []

    def list(self) -> list[Assignment]:
        return self._assignments.copy()

    def add(self, assignment: Assignment) -> None:
        self._assignments.append(assignment)

    def replace(self, index: int, assignment: Assignment) -> bool:
        if not 0 <= index < len(self._assignments):
            return False
        self._assignments[index] = assignment
        return True

    def delete(self, index: int) -> bool:
        if not 0 <= index < len(self._assignments):
            return False
        self._assignments.pop(index)
        return True
