from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.media.infrastructure.repository import MediaRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class MediaUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session_factory=session_factory)

    @property
    def media(self) -> MediaRepository:
        return MediaRepository(self._session)
