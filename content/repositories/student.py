from models import Course, User
from strategies.student import IStudentQueryStrategy
from dal.postgres import IDAL
from . import IRoleRepository
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
from strategies.student import get_student_strategy, StudentQueryStrategy
from fastapi import Depends


class StudentRepository(IRoleRepository):
    """Repository for handling student-specific data access."""

    def __init__(
            self, 
            strategy: IStudentQueryStrategy,
            dal: IDAL = None,
            session: AsyncSession = None):
        self.strategy = strategy
        self.dal = dal
        self.session = session

    async def get_courses(self, user: User) -> list[Course]:
        """Fetch courses for a student."""
        query = await self.strategy.get_courses(user)
        return (await self.dal.execute(query)).scalars().all()


def get_student_repository(
        ) -> IRoleRepository:
    return StudentRepository(
        strategy=StudentQueryStrategy(),
    )
