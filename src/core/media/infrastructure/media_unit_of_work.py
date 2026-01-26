from sqlalchemy.ext.asyncio import AsyncSession

from src.core.media.infrastructure.repository import MediaRepository
from src.core.shared.infrastructure.sql_alchemy_uow import SQLAlchemyUnitOfWork


class MediaUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    @property
    def media(self):
        return MediaRepository(self._session)
