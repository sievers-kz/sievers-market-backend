from _contextvars import ContextVar
from typing import AsyncGenerator

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

_session_ctx: ContextVar[AsyncSession] = ContextVar("database_session")


def get_current_session() -> AsyncSession:
    try:
        return _session_ctx.get()
    except LookupError:
        raise RuntimeError("database_session вызван вне контекста HTTP-запроса, теста или ARQ-задачи")


@inject
async def provide_database_session(
    session_factory: async_sessionmaker[AsyncSession] = Depends(Provide["gateways.session_factory"]),
) -> AsyncGenerator[None, None]:
    async with session_factory() as session:
        token = _session_ctx.set(session)
        try:
            yield
        finally:
            _session_ctx.reset(token)
