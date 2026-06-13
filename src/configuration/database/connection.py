from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


async def get_database_session(session_factory: Callable[[], AsyncSession]):
    async with session_factory() as session:
        yield session
