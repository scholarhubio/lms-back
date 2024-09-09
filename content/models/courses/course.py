from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import ContentBaseModel


class Course(ContentBaseModel):
    __tablename__ = 'courses_course'

    lessons_per_day: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    course_modules: Mapped[list['CourseModule']] = relationship('CourseModule', back_populates='course', cascade='all, delete-orphan')

    async def save(self, session: AsyncSession) -> None:
        """Asynchronously save the Course instance."""
        session.add(self)
        await session.commit()

    def __str__(self) -> str:
        return self.title
