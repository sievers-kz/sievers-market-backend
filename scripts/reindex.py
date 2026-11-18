"""Полная переиндексация объявлений: индекс пересобирается из Postgres.

Нужна после изменения формата документа или флагов `filterable`, а также если индекс разошёлся с базой.
При обычной работе индекс обновляют сами use case'ы (`sync_listing`), этот скрипт запускается вручную:
`make reindex` локально, `docker exec <контейнер backend> python -m scripts.reindex` на сервере.
"""

import asyncio

from meilisearch_python_sdk import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from scripts.search import build_listing_search_service
from src.configuration.settings.settings import MeilisearchConfig, PostgresSettings
from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.infrastructure.mapper import ListingMapper
from src.core.listing.infrastructure.models import Listing

BATCH_SIZE = 500


async def reindex(session: AsyncSession, service: ListingSearchService, batch_size: int = BATCH_SIZE) -> int:
    """Настройки индекса, очистка, затем все активные объявления пачками. Возвращает число документов.

    Очистка убирает документы, которых не должно быть (неактивные, удалённые, старого формата);
    поиск пустой только на время переиндексации.
    """
    await service.sync_schema()
    await service.clear_index()

    total = 0
    offset = 0
    while True:
        statement = (
            select(Listing)
            .where(Listing.status == ListingStatus.ACTIVE)
            .order_by(Listing.created_at, Listing.id)
            .offset(offset)
            .limit(batch_size)
        )
        rows = (await session.execute(statement)).scalars().all()
        if not rows:
            break

        total += await service.index_listings([ListingMapper.to_domain(row) for row in rows])
        offset += batch_size

    return total


async def main():
    engine = create_async_engine(url=PostgresSettings().database_url, echo=False)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    meili_settings = MeilisearchConfig()

    async with session_factory() as session, AsyncClient(url=meili_settings.url, api_key=meili_settings.key) as client:
        total = await reindex(session, build_listing_search_service(session, client))

    await engine.dispose()
    print(f"✅ Reindexed {total} listings")


if __name__ == "__main__":
    asyncio.run(main())
