from fastapi.testclient import TestClient

from assignment_tracker.app import app
from assignment_tracker.domain import Assignment, GradedAssignment
from assignment_tracker.infrastructure.adapters.in_memory_assignment_repository import InMemoryAssignmentRepository
from assignment_tracker.interface.api.dependencies import repositories


def test_assignment_object() -> None:
    assignment = Assignment("Finish Python project", "IT 545")
    assert "pending" in assignment.summary()
    assignment.complete()
    assert assignment.completed is True


def test_inheritance_and_polymorphism() -> None:
    assignments: list[Assignment] = [Assignment("Essay", "English"), GradedAssignment("Test", "IT 545", 20)]
    assert "20 points" in assignments[1].summary()
    assert "pending" in assignments[0].summary()


def test_crud_api() -> None:
    repositories.assignment_repository = InMemoryAssignmentRepository()
    with TestClient(app) as client:
        assert client.get("/health/").json() == {"status": "ok"}
        response = client.post("/v1/assignment/", json={"title": "Read chapter", "course": "IT 545"})
        assert response.status_code == 201
        assert len(response.json()["data"]) == 1
        assert client.get("/v1/assignment/?course=IT").status_code == 200
        response = client.patch("/v1/assignment/0", json={"completed": True})
        assert response.json()["data"][0]["completed"] is True
        response = client.put("/v1/assignment/0", json={"title": "Submit report", "course": "IT 545"})
        assert response.json()["data"][0]["title"] == "Submit report"
        assert client.delete("/v1/assignment/0").json()["data"] == []
        assert client.delete("/v1/assignment/0").status_code == 404


def test_invalid_data() -> None:
    repositories.assignment_repository = InMemoryAssignmentRepository()
    with TestClient(app) as client:
        assert client.post("/v1/assignment/", json={"title": "", "course": "IT 545"}).status_code == 422
        assert client.get("/v1/assignment/?limit=-1").status_code == 422
        assert client.patch("/v1/assignment/15", json={"title": "New"}).status_code == 404
