from abc import ABC, abstractmethod
from models import Course, User
from dal.postgres import IDAL

class IRoleRepository(ABC):
    """Repository for handling student-specific data access."""

    def __init__(self, session, dal: IDAL) -> None:
        self.session = session
        self.dal = dal

    @abstractmethod
    async def get_courses(self, user: User) -> list[Course]:
        pass
