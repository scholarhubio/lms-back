from abc import ABC, abstractmethod
from models.courses.moduls import Course, Module, Unit, Task
from models.courses.result import UserModuleSession, UserUnitSession, UserTaskSession, UserAnswer
from models.users.models import User
from uuid import UUID


class IQueryStrategy(ABC):
    """Interface for student-based query strategies."""

    @abstractmethod
    async def get_courses(self, user: User) -> list[Course]:
        """Fetch courses based on user role."""
        pass

    @abstractmethod
    async def get_modules(self, course_id: UUID) -> list[Module]:
        """Fetch modules based on course."""
        pass

    @abstractmethod
    async def get_units(self, module_id: UUID) -> list[Unit]:
        """Fetch units based on module."""
        pass

    @abstractmethod
    async def get_tasks(self, unit_id: UUID) -> list[Task]:
        """Fetch units based on module."""
        pass

    @abstractmethod
    async def get_task_by_answer(self, answer_id: UUID) -> Task:
        """Fetch task based on answer."""
        pass

    @abstractmethod
    async def get_user_module_session(self, module_id: UUID, user_id: UUID) -> UserModuleSession:
        pass

    @abstractmethod
    async def get_user_unit_session(self, unit_id: UUID, user_id: UUID) -> UserUnitSession:
        pass

    @abstractmethod
    async def get_user_task_session(self, task_id: UUID, user_id: UUID) -> UserTaskSession:
        pass

    @abstractmethod
    async def module_unit_task_by_answer(self, answer_id: UUID, user_id: UUID):
        pass

    @abstractmethod
    async def start_user_module_session(self, module_id: UUID, tries: int, user_id: UUID) -> UserModuleSession:
        pass

    @abstractmethod
    async def start_user_unit_session(self, unit_id: UUID, tries: int, user_id: UUID,) -> UserUnitSession:
        pass

    @abstractmethod
    async def start_user_task_session(self, task_id: UUID,tries: int, user_id: UUID) -> UserTaskSession:
        pass
    
    @abstractmethod
    async def create_user_answer(self, answer_id: UUID, user_id: UUID, session_id: UUID, is_correct: bool, answer_text: str) -> bool:
        pass

    @abstractmethod
    async def get_task_highest_parent(self, task_id: UUID) -> Task:
        pass

    @abstractmethod
    async def get_answer(self, answer_id: UUID) -> UserAnswer:
        pass

    @abstractmethod
    async def create_user_model_session(self, module_id: UUID, user_id: UUID):
        pass
    
    @abstractmethod
    async def get_user_module_session(self, module_id: UUID, user_id: UUID) -> UserModuleSession:
        pass

    @abstractmethod
    async def get_task(self, task_id: UUID) -> Task:
        pass
