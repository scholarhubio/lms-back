from abc import ABC, abstractmethod
from fastapi import Depends
from schemas.user import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_async_session
from repositories import IRoleRepository
from dal.postgres import get_postgres_dal, IDAL
from factories import get_role_repo_factory, IRoleRepositoryFactory
from models.users.models import User
from models.courses.result import UserUnitSession
from models.courses.moduls import Unit
from services.auth import get_current_user
from uuid import UUID


class IUnitService(ABC):
    @abstractmethod
    async def get_units(self, module_id: UUID):
        pass


class UnitService(IUnitService):
    def __init__(
            self,
            user: User,
            session: AsyncSession,
            repository: IRoleRepository,
            ) -> None:
        self.user = user
        self.repository = repository
        self.session = session
        self.repository.session = self.session

    async def get_units(self, module_id: UUID):
        await self.create_user_module_session(module_id=module_id)
        units = await self.repository.get_units(module_id=module_id)
        return units#await self.add_status(units)

    async def create_user_module_session(self, module_id: UUID):
        await self.repository.create_user_module_session(module_id=module_id, user_id=self.user.id)

    async def add_status(self, units: list[Unit]):
        datum = []
        unstarted_units_counter = 0
        for unit in units:
            data = {}
            user_unit_session = await self.repository.get_user_unit_session(unit_id=unit.id, user_id=self.user.id)
            data = {
                'title': unit.title,
                'id': unit.id,
            }
            data['complition'], data['stars'], counter = await self.define_status(user_unit_session)
            unstarted_units_counter += counter
            datum.append(data)
        return await self.open_first_element(units, unstarted_units_counter, datum)

    async def define_status(self, user_unit_session: UserUnitSession | None):
        if not user_unit_session:
            return None, 0, 1
        else:
            return user_unit_session.complition, user_unit_session.stars, 0

    async def open_first_element(self, units: list[Unit], unstarted_units_counter, datum: list[dict]):
        if len(units) > 0 and len(units) == unstarted_units_counter:
            datum[0]['complition'] = 'start'
        return datum


async def get_unit_service(
        fact: IRoleRepositoryFactory = Depends(get_role_repo_factory),
        session: AsyncSession = Depends(get_async_session),
        dal: IDAL = Depends(get_postgres_dal),
        user: User = Depends(get_current_user),):
    repo = await fact.get_repository(UserSchema(role=user.role))
    dal.session = session
    repo.dal = dal
    return UnitService(
        repository=repo,
        user=user,
        session=session,
    )
