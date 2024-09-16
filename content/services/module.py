from abc import ABC, abstractmethod
from fastapi import Depends
from schemas.user import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_async_session
from repositories import IRoleRepository
from dal.postgres import get_postgres_dal, IDAL
from factories import get_role_repo_factory, IRoleRepositoryFactory
from models.users.models import User
from models.courses.moduls import Module
from models.courses.result import UserModuleSession
from services.auth import get_current_user
from uuid import UUID


class IModuleService(ABC):
    @abstractmethod
    async def get_modules(self, course_id: UUID):
        pass


class ModuleService(IModuleService):
    def __init__(
            self, user,
            session: AsyncSession,
            repository: IRoleRepository,
            ) -> None:
        self.user = user
        self.repository = repository
        self.session = session
        self.repository.session = self.session

    async def get_modules(self, course_id: UUID):
        modules = await self.repository.get_modules(course_id=course_id, user_id=self.user.id)
        return modules
            
    async def add_status(self, modules: list[Module]):
        datum = []
        unstarted_modules_counter = 0
        for module in modules:
            data = {}
            user_module_session = await self.repository.get_user_module_session(module_id=module.id, user_id=self.user.id)
            data = {
                'title': module.title,
                'id': module.id,
            }
            data['complition'], data['stars'], counter = await self.define_status(user_module_session)
            unstarted_modules_counter += counter
            datum.append(data)
        return await self.open_first_element(modules, unstarted_modules_counter, datum)
    
    async def define_status(self, user_module_session: UserModuleSession | None):
        if not user_module_session:
            return None, 0, 1
        else:
            return user_module_session.complition, user_module_session.stars, 0
        
    async def open_first_element(self, modules: list[Module], unstarted_modules_counter, datum: list[dict]):
        if len(modules) > 0 and len(modules) == unstarted_modules_counter:
            datum[0]['complition'] = 'start'
        return datum


async def get_module_service(
        fact: IRoleRepositoryFactory = Depends(get_role_repo_factory),
        session: AsyncSession = Depends(get_async_session),
        dal: IDAL = Depends(get_postgres_dal),
        user: User = Depends(get_current_user),):
    repo = await fact.get_repository(UserSchema(role=user.role))
    dal.session = session
    repo.dal = dal
    return ModuleService(
        repository=repo,
        user=user,
        session=session,
    )
