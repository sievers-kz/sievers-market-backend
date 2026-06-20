from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.media.application.interfaces.repository import IMediaRepository
from src.core.media.domain.entities import Media as DomainMedia
from src.core.media.infrastructure.mapper import MediaMapper
from src.core.media.infrastructure.models import Media as ORMMedia


class MediaRepository(IMediaRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = ORMMedia

    async def save(self, media: list[DomainMedia]) -> None:
        mapped_model = MediaMapper.to_orm(media)
        self._session.add_all(mapped_model)
        await self._session.flush()

    async def delete(self, media_id: UUID) -> None:
        statement = delete(self.model).where(self.model.id == media_id)
        await self._session.execute(statement)
        await self._session.flush()
