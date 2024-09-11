from abc import ABC, abstractmethod
from fastapi import Depends
from schemas.user import UserSchema
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_async_session
from repositories import IRoleRepository
from dal.postgres import get_postgres_dal, IDAL
from factories import get_role_repo_factory, IRoleRepositoryFactory
from models.users import User
from models.courses.tasks import Task, UserTaskSession
from services.auth import get_current_user
from uuid import UUID
from exceptions import TaskAnswered


class ITaskService(ABC):
    @abstractmethod
    async def get_tasks(self, unit_id: UUID):
        pass

    @abstractmethod
    async def get_task(self, task_id: UUID):
        pass

    @abstractmethod
    async def create_user_task_session(self, task_id: UUID) -> UserTaskSession:
        pass


class TaskService(ITaskService):
    def __init__(
            self, user: User,
            session: AsyncSession,
            repository: IRoleRepository,
            ) -> None:
        self.user = user
        self.repository = repository
        self.session = session
        self.repository.session = self.session

    async def get_tasks(self, unit_id: UUID) -> list[Task]:
        await self.repository.get_or_create_user_unit_session(unit_id, self.user.id)
        tasks = await self.repository.get_tasks(unit_id=unit_id)
        return await self.add_status(tasks)

    async def get_task(self, task_id: UUID) -> Task:
        return await self.repository.get_task(task_id=task_id, user_id=self.user.id)

    async def create_user_task_session(self, task_id: UUID) -> UserTaskSession:
        is_created, result = await self.repository.get_or_create_user_task_session(task_id, self.user.id)
        if is_created == False:
            raise TaskAnswered
        return result

    async def add_status(self, tasks: list[Task]):
        datum = []
        unstarted_tasks_counter = 0
        for task in tasks:
            data = {}
            user_task_session = await self.repository.get_user_task_session(task_id=task.id, user_id=self.user.id)
            data = {
                'title': task.title,
                'id': task.id,
            }
            data['complition'], data['stars'], counter = await self.define_status(user_task_session)
            unstarted_tasks_counter += counter
            datum.append(data)
        return await self.open_first_element(tasks, unstarted_tasks_counter, datum)

    async def define_status(self, user_task_session: UserTaskSession | None):
        if not user_task_session:
            return None, 0, 1
        else:
            return user_task_session.complition, user_task_session.stars, 0

    async def open_first_element(self, tasks: list[Task], unstarted_tasks_counter, datum: list[dict]):
        if len(tasks) > 0 and len(tasks) == unstarted_tasks_counter:
            datum[0]['complition'] = 'start'
        return datum


async def get_task_service(
        fact: IRoleRepositoryFactory = Depends(get_role_repo_factory),
        session: AsyncSession = Depends(get_async_session),
        dal: IDAL = Depends(get_postgres_dal),
        user: User = Depends(get_current_user),):
    repo = await fact.get_repository(UserSchema(role=user.role))
    dal.session = session
    repo.dal = dal
    return TaskService(
        repository=repo,
        user=user,
        session=session,
    )
