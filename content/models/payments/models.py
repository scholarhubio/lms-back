from sqlalchemy import ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel
from datetime import date
from uuid import UUID


class Subscription(BaseModel):
    __tablename__ = 'payments_subscription'
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users_user.id'), unique=True, nullable=False)
    course_module_id: Mapped[UUID] = mapped_column(ForeignKey('courses_course_module.id'), unique=True, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, default=date.today())
    end_date: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user: Mapped['User'] = relationship('User', back_populates='subscriptions')
    course_module: Mapped['CourseModule'] = relationship('CourseModule', back_populates='subscriptions')
