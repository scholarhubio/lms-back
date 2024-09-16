from abc import ABC, abstractmethod
from fastapi import Depends
from schemas.user import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_async_session
from repositories import IRoleRepository
from dal.postgres import get_postgres_dal, IDAL
from factories import get_role_repo_factory, IRoleRepositoryFactory
from models.users.models import User
from services.auth import get_current_user


class ICourseService(ABC):

    @abstractmethod
    async def get_courses(self):
        pass


class CourseService(ICourseService):
    def __init__(
            self, user,
            session: AsyncSession,
            repository: IRoleRepository,
            ) -> None:
        self.user = user
        self.repository = repository
        self.session = session
        self.repository.session = self.session

    async def get_courses(self):
        return await self.repository.get_courses(user=self.user)


async def get_course_service(
        fact: IRoleRepositoryFactory = Depends(get_role_repo_factory),
        session: AsyncSession = Depends(get_async_session),
        dal: IDAL = Depends(get_postgres_dal),
        user: User = Depends(get_current_user),):
    repo = await fact.get_repository(UserSchema(role=user.role))
    dal.session = session
    repo.dal = dal
    return CourseService(
        repository=repo,
        user=user,
        session=session,
    )
