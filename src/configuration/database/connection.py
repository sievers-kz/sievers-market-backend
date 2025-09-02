from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


async def get_async_session(session_maker: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
