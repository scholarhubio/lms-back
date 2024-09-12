from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from models import User

class IUserStorage(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_phone(self, phone: str, session: AsyncSession) -> Optional[User]:
        pass

    @abstractmethod
    async def create_new_user(self, phone: str, password: str, session: AsyncSession) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        pass
