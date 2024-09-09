from abc import ABC, abstractmethod
from typing import Any
from sqlalchemy.orm import Query, Session
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult


class IDAL(ABC):
    """Interface for Data Access Layer."""

    def __init__(self, session = None) -> None:
        self.session = session

    @abstractmethod
    async def execute(self, query: Query) -> AsyncResult:
        pass

    @abstractmethod
    async def commit(self, session: AsyncSession) -> None:
        pass

    @abstractmethod
    async def delete(self, session: AsyncSession) -> None:
        pass


class PostgresDAL(IDAL):
    """Data Access Layer that uses injected queries."""
    """Centralized session handler for managing database interactions."""
    def __init__(self, session: AsyncSession = None) -> None:
        self.session = session

    async def execute(self, query: Query) -> Session:
        """Execute a query and return results."""
        async with self.session.begin():
            result = await self.session.execute(query)
        return result

    async def commit(self) -> None:
        """Commit the current transaction."""
        async with self.session.begin():
            await self.session.commit()

    async def delete(self, instance: object) -> None:
        """Delete an instance from the current session."""
        async with self.session.begin():
            await self.session.delete(instance)


async def get_postgres_dal() -> IDAL:
    return PostgresDAL()
