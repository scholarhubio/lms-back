from models import Course, User, UserModuleSession, Task, UserTaskSession, UserUnitSession, UserAnswer
from interfaces.strategy import IQueryStrategy
from dal.postgres import IDAL
from . import IRoleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from strategies.student import StudentQueryStrategy
from uuid import UUID
from exceptions import NotFound, AlreadyChoosen


class StudentRepository(IRoleRepository):
    """Repository for handling student-specific data access."""

    def __init__(
            self, 
            strategy: IQueryStrategy,
            dal: IDAL = None,
            session: AsyncSession = None):
        self.strategy = strategy
        self.dal = dal
        self.session = session

    async def get_courses(self, user: User) -> list[Course]:
        """Fetch courses for a student."""
        query = await self.strategy.get_courses(user)
        return (await self.dal.execute(query)).scalars().all()

    async def get_modules(self, course_id: UUID, user_id: UUID) -> list[Course]:
        """Fetch course modules for a student."""
        query = await self.strategy.get_modules(course_id, user_id)
        return (await self.dal.execute(query)).scalars().all()
    
    async def get_units(self, module_id: UUID) -> list[Course]:
        """Fetch course modules for a student."""
        query = await self.strategy.get_units(module_id)
        return (await self.dal.execute(query)).scalars().all()
    
    async def get_tasks(self, unit_id: UUID) -> list[Course]:
        """Fetch course modules for a student."""
        query = await self.strategy.get_tasks(unit_id)
        return (await self.dal.execute(query)).scalars().all()

    async def get_or_create_user_module_session(self, module_id: UUID, user_id: UUID) -> UserModuleSession:
        query = await self.strategy.get_user_module_session(module_id, user_id)
        result = (await self.dal.execute(query)).fetchone()
        if bool(result) == False:
            result = await self.strategy.start_user_module_session(user_id=user_id, module_id=module_id, tries=0)
            self.session.add(result)
            await self.session.commit()
            await self.session.refresh(result)
        return bool(result), result

    async def task_by_answer(self, answer_id: UUID) -> Task:
        query = await self.strategy.get_task_by_answer(answer_id=answer_id)
        return (await self.dal.execute(query)).scalar_one_or_none()

    async def get_user_unit_session(self, unit_id: UUID, user_id: UUID):
        query = await self.strategy.get_user_unit_session(unit_id, user_id)
        return (await self.dal.execute(query)).scalar_one_or_none()

    async def get_or_create_user_unit_session(self, unit_id: UUID, user_id: UUID) -> UserUnitSession:
        result = await self.get_user_unit_session(unit_id, user_id)
        if not result:
            result = await self.strategy.start_user_unit_session(user_id=user_id, unit_id=unit_id, tries=0)
            self.session.add(result)
            async with self.session:
                await self.session.commit()
                await self.session.refresh(result)
        return bool(result), result

    async def get_or_create_user_task_session(self, task_id: UUID, user_id: UUID) -> UserTaskSession:
        result = await self.get_user_task_session(task_id, user_id)
        if not result:
            result = await self.strategy.start_user_task_session(user_id=user_id, task_id=task_id, tries=0)
            self.session.add(result)
            async with self.session:
                await self.session.commit()
                await self.session.refresh(result)
        return bool(result), result

    async def get_user_task_session(self, task_id: UUID, user_id: UUID) -> UserTaskSession:
        query = await self.strategy.get_user_task_session(task_id, user_id)
        return (await self.dal.execute(query)).scalar()

    async def module_unit_task_by_answer(self, answer_id: UUID, user_id: UUID):
        query = await self.strategy.module_unit_task_by_answer(answer_id, user_id)
        return ()

    async def create_user_answer(self, answer_id: UUID, user_id: UUID) -> UserAnswer:
        answer_qr = await self.strategy.get_answer(answer_id)
        answer = (await self.dal.execute(answer_qr)).scalar_one_or_none()
        if not answer:
            raise NotFound
        task = await self.task_by_answer(answer_id=answer.id)
        parent_task_qr = await self.strategy.get_task_highest_parent(task_id=task.id)
        parent_task = (await self.dal.execute(parent_task_qr)).scalar_one_or_none()
        if parent_task:
            task = parent_task
        task_session_qr = await self.strategy.get_user_task_session(
            user_id=user_id, task_id=task.id)
        task_session = (await self.dal.execute(task_session_qr)).scalar_one_or_none()
        if not task_session:
            task_session = await self.strategy.start_user_task_session(
                task_id=task.id,
                user_id=user_id,
                tries=0,
            )
            self.session.add(task_session)
            await self.session.flush()
        task_answer = await self.strategy.create_user_answer(
            answer_id=answer.id,
            user_id=user_id,
            session_id=task_session.id,
            answer_text=answer.text,
            is_correct=answer.is_correct,)
        self.session.add(task_answer)
        try:
            async with self.session:
                await self.session.commit()
                await self.session.refresh(task_answer)
        except IntegrityError:
            raise AlreadyChoosen
        return task_answer

    async def create_user_module_session(self, user_id: UUID, module_id: UUID):
        user_module_session = await self.get_user_module_session(module_id=module_id, user_id=user_id)
        if bool(user_module_session) == True:
            return user_module_session
        user_module_session = await self.strategy.create_user_model_session(
            user_id=user_id, module_id=module_id)

        self.session.add(user_module_session)
        await self.session.commit()
        return user_module_session
    
    async def get_user_module_session(self, module_id: UUID, user_id: UUID) -> UserModuleSession:
        user_module_session_qr = await self.strategy.get_user_module_session(module_id, user_id)
        return (await self.dal.execute(user_module_session_qr)).scalar_one_or_none()

    async def get_task(self, task_id: UUID, user_id):
        task_qr = await self.strategy.get_task(task_id)
        return (await self.dal.execute(task_qr)).scalar_one_or_none()


def get_student_repository(
        ) -> IRoleRepository:
    return StudentRepository(
        strategy=StudentQueryStrategy(),
    )
