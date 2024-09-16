from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum
from typing import Optional
from models.base import ContentBaseModel, OrderedModel, BaseModel
from models.courses.choices import TaskType, ItemType
import uuid


class Task(BaseModel, OrderedModel):
    __tablename__ = 'courses_task'

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey('courses_task.id'), nullable=True, default=None
    )
    unit_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('courses_unit.id'), nullable=False)
    type: Mapped[str] = mapped_column(String(10), SQLAlchemyEnum(TaskType), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    parent: Mapped[Optional['Task']] = relationship('Task', back_populates='children', remote_side='Task.id')
    children: Mapped[list['Task']] = relationship('Task', back_populates='parent', cascade='all, delete-orphan')
    unit: Mapped['Unit'] = relationship('Unit', back_populates='tasks')
    items: Mapped[list['TaskItem']] = relationship('TaskItem', back_populates='task', cascade='all, delete-orphan')
    answers: Mapped[list['Answer']] = relationship('Answer', back_populates='task', cascade='all, delete-orphan')
    sessions: Mapped[list['UserTaskSession']] = relationship('UserTaskSession', back_populates='task', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return f'Task {self.type} {self.unit_id}'


class TaskItem(BaseModel):
    __tablename__ = 'courses_taskitem'

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('courses_task.id'), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    video: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(SQLAlchemyEnum(ItemType), nullable=False)

    task: Mapped['Task'] = relationship('Task', back_populates='items')

    def __str__(self) -> str:
        return f'TaskItem for Task ID: {self.task_id}'


class Answer(BaseModel):
    __tablename__ = 'courses_answer'

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('courses_task.id'), nullable=False)
    sign: Mapped[str] = mapped_column(String(10))
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    manual: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    user_answer: Mapped['UserAnswer'] = relationship('UserAnswer', back_populates='answer')
    task: Mapped['Task'] = relationship('Task', back_populates='answers')

    def __str__(self) -> str:
        return f'Answer for Task ID: {self.task_id}'
