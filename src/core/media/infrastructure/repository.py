from uuid import UUID

from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.media.application.interfaces.abstract_media_repository import AbstractMediaRepository
from src.core.media.infrastructure.mapper import MediaMapper
from src.core.media.infrastructure.models import Media as ORMMedia
from src.core.media.domain.entities import Media as DomainMedia


class MediaRepository(AbstractMediaRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._media = ORMMedia

    async def save(self, media: DomainMedia):
        mapped_model = MediaMapper.to_orm(media)
        if isinstance(mapped_model, list):
            self._session.add_all(mapped_model)
        else:
            await self._session.merge(mapped_model)
        await self._session.flush()

    async def delete_by_ids(self, media_ids: list[UUID]):
        if not media_ids:
            return

        statement = delete(self._media).where(self._media.id.in_(media_ids))
        await self._session.execute(statement)

    async def get_max_position(self, machinery_id: UUID) -> int:
        statement = select(func.max(self._media.position)).where(self._media.machinery_id == machinery_id)
        result = await self._session.execute(statement)
        max_position = result.scalar()
        return max_position if max_position is not None else -1

    async def get_media_by_machinery_id(self, machinery_id: UUID) -> list[DomainMedia]:
        statement = select(self._media).where(self._media.machinery_id == machinery_id)
        query_result = await self._session.execute(statement)
        orm_model = query_result.scalars().all()

        if not orm_model:
            return []

        return MediaMapper.to_domain(orm_model)

