class Assignment:
    def __init__(self, title: str, course: str, completed: bool = False) -> None:
        if not title.strip():
            raise ValueError("An assignment needs a title")
        if not course.strip():
            raise ValueError("An assignment needs a course")
        self.title = title
        self.course = course
        self.completed = completed

    def complete(self) -> None:
        self.completed = True

    def summary(self) -> str:
        state = "completed" if self.completed else "pending"
        return f"{self.title} ({self.course}) - {state}"


class GradedAssignment(Assignment):
    def __init__(self, title: str, course: str, points: int) -> None:
        super().__init__(title, course)
        if points <= 0:
            raise ValueError("Points must be positive")
        self.points = points

    def summary(self) -> str:
        return f"{super().summary()} - {self.points} points"
