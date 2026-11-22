"""Настройки индекса поиска (`sync_schema`). Запускается в `entrypoint.sh` при каждом старте контейнера."""

import asyncio

from meilisearch_python_sdk import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.configuration.settings.settings import MeilisearchConfig, PostgresSettings
from src.core.catalog.infrastructure.catalog_service import CatalogService
from src.core.catalog.infrastructure.repositories.attributes import SubcategoryAttributeRepository
from src.core.catalog.infrastructure.repositories.categories import (
    CategoryRepository,
    SubcategoryRepository,
)
from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.shared.infrastructure.services.meilisearch_service import (
    MeilisearchService,
)


def build_listing_search_service(session: AsyncSession, client: AsyncClient) -> ListingSearchService:
    """Сервис поиска для скриптов: те же классы, что в приложении, но без DI-контейнера."""
    catalog_service = CatalogService(
        category_repo=CategoryRepository(session),
        subcategory_repo=SubcategoryRepository(session),
        link_repo=SubcategoryAttributeRepository(session),
    )
    return ListingSearchService(search_service=MeilisearchService(client), catalog_service=catalog_service)


async def main():
    engine = create_async_engine(url=PostgresSettings().database_url, echo=False)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    meili_settings = MeilisearchConfig()

    async with session_factory() as session, AsyncClient(url=meili_settings.url, api_key=meili_settings.key) as client:
        await build_listing_search_service(session, client).sync_schema()

    await engine.dispose()
    print("✅ Search schema synced")


if __name__ == "__main__":
    asyncio.run(main())
