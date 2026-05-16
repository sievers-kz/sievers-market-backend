from typing import AsyncGenerator, Callable
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


async def get_database_session(session_factory: Callable[[], AsyncSession]):
    async with session_factory() as session:
        yield session


