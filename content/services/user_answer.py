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
from uuid import UUID
from schemas.responses.user_answer import AnswerResponse


class IUserAnswerService(ABC):

    @abstractmethod
    async def create_user_answer(self, answer_id: UUID):
        pass

class UserAnswerService(IUserAnswerService):
    def __init__(
            self, user: User,
            session: AsyncSession,
            repository: IRoleRepository,
            ) -> None:
        self.user = user
        self.repository = repository
        self.session = session
        self.repository.session = self.session

    async def create_user_answer(self, answer_id: UUID):
        user_answer = await self.repository.create_user_answer(answer_id, self.user.id)
        if user_answer.is_correct == True:
            return AnswerResponse(detail='Correct Answer', is_correct=True)
        return AnswerResponse(detail='Incorrect Answer', is_correct=False)


async def get_user_answer_service(
        fact: IRoleRepositoryFactory = Depends(get_role_repo_factory),
        session: AsyncSession = Depends(get_async_session),
        dal: IDAL = Depends(get_postgres_dal),
        user: User = Depends(get_current_user),):
    repo = await fact.get_repository(UserSchema(role=user.role))
    dal.session = session
    repo.dal = dal
    return UserAnswerService(
        repository=repo,
        user=user,
        session=session,
    )
