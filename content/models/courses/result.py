from sqlalchemy import Text, Boolean, ForeignKey, SmallInteger, types, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.types import Enum as SQLAlchemyEnum
from models.courses.choices import TaskCompletionType, TaskResultType
from datetime import datetime
from typing import Optional
from models import BaseModel
from uuid import UUID


class BaseContentSessionModel(BaseModel):
    """Session model with start, finish times, stars, completion, and result."""

    __abstract__ = True

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    stars: Mapped[int] = mapped_column(Integer, default=0)
    complition: Mapped[TaskCompletionType] = mapped_column(SQLAlchemyEnum(TaskCompletionType), nullable=False)
    result: Mapped[TaskResultType] = mapped_column(SQLAlchemyEnum(TaskResultType), nullable=False)


# Define the UserAnswer model
class UserAnswer(BaseModel):
    __tablename__ = 'courses_useranswer'

    user_id: Mapped[UUID] = mapped_column(types.UUID, unique=True, nullable=False)
    session_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_usertasksession.id'), nullable=True)
    answer_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_answer.id'), nullable=True)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    session: Mapped[Optional['UserTaskSession']] = relationship('UserTaskSession', back_populates='answers')
    answer: Mapped[Optional['Answer']] = relationship('Answer', back_populates='user_answers')

    async def save(self, session: AsyncSession) -> None:
        """Asynchronously save the UserAnswer instance."""
        session.add(self)
        await session.commit()

    def __str__(self) -> str:
        return f'User Answer: {self.answer_text[:30]}...'


# Define the UserTaskSession model
class UserTaskSession(BaseContentSessionModel):
    __tablename__ = 'courses_usertasksession'

    task_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_task.id'), nullable=True)
    tries: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    task: Mapped[Optional['Task']] = relationship('Task')  # Assuming the 'Task' model exists
    answers: Mapped[list['UserAnswer']] = relationship('UserAnswer', back_populates='session', cascade='all, delete-orphan')

    async def save(self, session: AsyncSession) -> None:
        """Asynchronously save the UserTaskSession instance."""
        session.add(self)
        await session.commit()

    def __str__(self) -> str:
        return f'Task Session for Task ID: {self.task_id}'


# Define the UserUnitSession model
class UserUnitSession(BaseContentSessionModel):
    __tablename__ = 'courses_userunitsession'

    unit_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_unit.id'), nullable=True)

    unit: Mapped[Optional['Unit']] = relationship('Unit')  # Assuming the 'Unit' model exists

    async def save(self, session: AsyncSession) -> None:
        """Asynchronously save the UserUnitSession instance."""
        session.add(self)
        await session.commit()

    def __str__(self) -> str:
        return f'Unit Session for Unit ID: {self.unit_id}'


# Define the UserModuleSession model
class UserModuleSession(BaseContentSessionModel):
    __tablename__ = 'courses_usermodulesession'

    module_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_module.id'), nullable=True)

    module: Mapped[Optional['Module']] = relationship('Module')  # Assuming the 'Module' model exists

    async def save(self, session: AsyncSession) -> None:
        """Asynchronously save the UserModuleSession instance."""
        session.add(self)
        await session.commit()

    def __str__(self) -> str:
        return f'Module Session for Module ID: {self.module_id}'
