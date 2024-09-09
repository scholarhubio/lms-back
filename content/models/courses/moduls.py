from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from models import ContentBaseModel, Course, OrderedModel, Task
from models.courses.choices import UnitType
from uuid import UUID


class Module(ContentBaseModel):
    __tablename__ = 'courses_module'

    module_courses: Mapped[list['CourseModule']] = relationship(
        'CourseModule', back_populates='module', cascade='all, delete-orphan'
    )
    units: Mapped[list['Unit']] = relationship('Unit', back_populates='module', cascade='all, delete-orphan')

    def __str__(self) -> str:
        return self.title


class Unit(ContentBaseModel):
    __tablename__ = 'courses_unit'

    module_id: Mapped[UUID] = mapped_column(ForeignKey('courses_module.id'), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default=UnitType.PAID.value)

    module: Mapped['Module'] = relationship('Module', back_populates='units')
    unit_item: Mapped['UnitItem'] = relationship('UnitItem', uselist=False, back_populates='unit', cascade='all, delete-orphan')
    tasks: Mapped[list['Task']] = relationship('Task', back_populates='unit', cascade='all, delete-orphan')
    def __str__(self) -> str:
        return f'Unit in {self.module.title}'


class UnitItem(ContentBaseModel):
    __tablename__ = 'courses_unititems'

    unit_id: Mapped[UUID] = mapped_column(ForeignKey('courses_unit.id'), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default='')

    unit: Mapped['Unit'] = relationship('Unit', back_populates='unit_item')

    def __str__(self) -> str:
        return f'Item of {self.unit.module.title} - {self.unit.title}'


class CourseModule(ContentBaseModel, OrderedModel):
    __tablename__ = 'course_coursemodule'

    course_id: Mapped[UUID] = mapped_column(ForeignKey('courses_course.id'), nullable=False)
    module_id: Mapped[UUID] = mapped_column(ForeignKey('courses_module.id'), nullable=False)  # Assuming the 'modules' table exists

    course: Mapped['Course'] = relationship('Course', back_populates='course_modules')
    module: Mapped['Module'] = relationship('Module', back_populates='module_courses')

    __table_args__ = (
        UniqueConstraint('course_id', 'order', name='unique_course_order'),
    )

    def get_ordering_scope(self) -> dict:
        """Defines the ordering scope for CourseModule."""
        return {
            'course_id': self.course_id,
            'module_id': self.module_id
        }
