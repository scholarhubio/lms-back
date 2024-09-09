from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import Depends


async_session_factory: sessionmaker | None = None
async_engine: AsyncEngine | None = None


def get_async_factory() -> sessionmaker:
    return async_session_factory


async def get_async_session(session_factory=Depends(get_async_factory)) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
                await session.rollback()
                raise e
        finally:
            await session.close()
