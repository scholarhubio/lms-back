# role_query_strategy_interface.py
from abc import ABC, abstractmethod
from models import User, Course
from sqlalchemy import select


class IStudentQueryStrategy(ABC):
    """Interface for student-based query strategies."""

    @abstractmethod
    async def get_courses(self, user: User) -> list[Course]:
        """Fetch courses based on user role."""
        pass


class StudentQueryStrategy(IStudentQueryStrategy):
    async def get_courses(self, user: User) -> list[Course]:
        return select(Course)


def get_student_strategy():
    return StudentQueryStrategy()
