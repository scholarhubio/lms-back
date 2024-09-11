from abc import ABC, abstractmethod
from models import Course, User, UserAnswer
from models.courses.moduls import Module, Unit, UserModuleSession
from models.courses.tasks import UserTaskSession
from models.courses.result import UserUnitSession
from dal.postgres import IDAL
from uuid import UUID


class IRoleRepository(ABC):
    """Repository for handling student-specific data access."""

    def __init__(self, session, dal: IDAL) -> None:
        self.session = session
        self.dal = dal

    @abstractmethod
    async def get_courses(self, user: User) -> list[Course]:
        pass

    @abstractmethod
    async def get_modules(self, course_id: UUID, user_id: UUID) -> list[Module]:
        pass

    @abstractmethod
    async def get_user_module_session(self, module_id: UUID, user_id: UUID) -> list[Module]:
        pass

    @abstractmethod
    async def get_units(self, module_id: UUID) -> list[Unit]:
        pass

    @abstractmethod
    async def get_tasks(self, unit_id: UUID) -> list[Unit]:
        pass

    @abstractmethod
    async def create_user_answer(self, answer_id: UUID, user_id: UUID) -> UserAnswer:
        pass

    @abstractmethod
    async def task_by_answer(self, answer_id: UUID):
        pass

    @abstractmethod
    async def create_user_module_session(self, user_id: UUID, module_id: UUID) -> None:
        pass

    @abstractmethod
    async def get_user_module_session(self, module_id: UUID, user_id: UUID) -> UserModuleSession:
        pass

    @abstractmethod
    async def get_user_unit_session(self, unit_id: UUID, user_id: UUID):
        pass

    @abstractmethod
    async def get_task(self, task_id: UUID, user_id):
        pass
    
    @abstractmethod
    async def get_user_task_session(self, task_id: UUID, user_id: UUID) -> UserTaskSession:
        pass

    @abstractmethod
    async def get_or_create_user_task_session(self, task_id: UUID, user_id: UUID) -> UserTaskSession:
        pass

    @abstractmethod
    async def get_or_create_user_unit_session(self, unit_id: UUID, user_id: UUID) -> UserUnitSession:
        pass
