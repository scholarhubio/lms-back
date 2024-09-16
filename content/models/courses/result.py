from sqlalchemy import Text, Boolean, ForeignKey, SmallInteger, types, DateTime, Integer, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum
from models.courses.choices import TaskCompletionType, TaskResultType
from datetime import datetime
from typing import Optional
from models import BaseModel
from models.courses.moduls import Module
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import aliased


class BaseContentSessionModel(BaseModel):
    """Session model with start, finish times, stars, completion, and result."""

    __abstract__ = True

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False), nullable=True)
    stars: Mapped[int] = mapped_column(Integer, default=0)
    complition: Mapped[TaskCompletionType] = mapped_column(String(25), SQLAlchemyEnum(TaskCompletionType), nullable=False, default=TaskCompletionType.STARTED.value)
    result: Mapped[TaskResultType] = mapped_column(String(25), SQLAlchemyEnum(TaskResultType), nullable=True)
    user_id: Mapped[UUID] = mapped_column(types.UUID, nullable=False)
    tries: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)


class UserAnswer(BaseModel):
    __tablename__ = 'courses_useranswer'

    user_id: Mapped[UUID] = mapped_column(types.UUID, nullable=False)
    session_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_usertasksession.id'), nullable=True)
    answer_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_answer.id'), nullable=True)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    session: Mapped[Optional['UserTaskSession']] = relationship('UserTaskSession', back_populates='answers')
    answer: Mapped[Optional['Answer']] = relationship('Answer', back_populates='user_answer')

    def __str__(self) -> str:
        return f'User Answer: {self.answer_text[:30]}...'


class UserTaskSession(BaseContentSessionModel):
    __tablename__ = 'courses_usertasksession'

    task_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_task.id'), nullable=True)
    task: Mapped[Optional['Task']] = relationship('Task', back_populates='sessions')  # Assuming the 'Task' model exists
    answers: Mapped[list['UserAnswer']] = relationship('UserAnswer', back_populates='session', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return f'Task Session for Task ID: {self.task_id}'


class UserUnitSession(BaseContentSessionModel):
    __tablename__ = 'courses_userunitsession'

    unit_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_unit.id'), nullable=True)
    unit: Mapped[Optional['Unit']] = relationship('Unit')  # Assuming the 'Unit' model exists


    def __str__(self) -> str:
        return f'Unit Session for Unit ID: {self.unit_id}'


class UserModuleSession(BaseContentSessionModel):
    __tablename__ = 'courses_usermodulesession'

    module_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('courses_module.id'), nullable=True)
    module: Mapped[Optional['Module']] = relationship('Module', back_populates='sessions')

    def __str__(self) -> str:
        return f'Module Session for Module ID: {self.module_id}'

    async def last_user_session_subquery(self, user_id: UUID):
        latest_session = aliased(UserModuleSession)
        # Subquery to get the latest session for each module for the given user
        return select(
                latest_session
            ).where(
                latest_session.module_id == Module.id,
                latest_session.user_id == user_id
            ).order_by(latest_session.created_at.desc()
                       ).limit(1).scalar_subquery()
