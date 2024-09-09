from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from interfaces.storage import IUserStorage


class UserStorage(IUserStorage):
    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> User | None:
        # Implement the logic to fetch a user by ID
        async with session:
            result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_phone(self, phone: str, session: AsyncSession) -> User | None:
        # Implement the logic to fetch a user by phone
        async with session:
            result = await session.execute(select(User).where(User.phone_number == phone))
        return result.scalar_one_or_none()

    async def create_new_user(self, phone: str, password: str, role, session: AsyncSession) -> User:
        new_user = User(phone_number=phone, password=password, role=role.value)
        async with session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        return new_user


async def get_user_storage() -> UserStorage:
    return UserStorage()
