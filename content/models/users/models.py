from sqlalchemy import String, Boolean, ForeignKey, Text, Date, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.types import Enum as SQLAlchemyEnum
from phonenumbers import parse, is_valid_number, NumberParseException
from models.base import BaseModel
from typing import Optional
from datetime import datetime, date
from models.users.choices import RoleType
from models.payments.models import Subscription
from uuid import UUID


class User(BaseModel):
    __tablename__ = 'users_user'

    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    date_joined: Mapped[date] = mapped_column(Date, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    password: Mapped[str] = mapped_column(String(255), unique=True)
    role: Mapped[RoleType] = Column(String(10), SQLAlchemyEnum(RoleType, create_type=True, name='roletype'), nullable=False)
    profile: Mapped[Optional['Profile']] = relationship('Profile', uselist=False, back_populates='user', cascade='all, delete-orphan')
    subscriptions: Mapped[list['Subscription']] = relationship('Subscription', back_populates='user')

    @validates('phone_number')
    def validate_phone_number(self, key: str, value: str) -> str:
        try:
            phone = parse(value)
            if not is_valid_number(phone):
                raise ValueError(f"Invalid phone number: {value}")
            return value
        except NumberParseException:
            raise ValueError(f"Invalid phone number format: {value}")

    def __str__(self) -> str:
        return f'{self.phone_number}-{self.id}'


class Profile(BaseModel):
    __tablename__ = 'users_profile'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users_user.id'), unique=True, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default='')
    location: Mapped[Optional[str]] = mapped_column(String(30), nullable=True, default='')
    birth_date: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Store avatar as a file path string

    user: Mapped['User'] = relationship('User', back_populates='profile')

    def __str__(self) -> str:
        return f'{self.user.username} Profile'
