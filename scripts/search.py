# scripts/sync_search_schema.py

import asyncio

from meilisearch_python_sdk import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import joinedload

from src.configuration.settings.settings import MeilisearchConfig, PostgresSettings
from src.core.catalog.infrastructure.models import SubcategoryAttribute
from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.shared.infrastructure.services.meilisearch_service import (
    MeilisearchService,
)


async def main():
    db_settings = PostgresSettings()
    meili_settings = MeilisearchConfig()

    engine = create_async_engine(url=db_settings.database_url, echo=False)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with session_factory() as session:
        statement = (
            select(SubcategoryAttribute)
            .where(SubcategoryAttribute.filterable.is_(True))
            .options(joinedload(SubcategoryAttribute.attribute))
        )
        result = await session.execute(statement)
        links = result.scalars().unique().all()
        dynamic_filterable = list({link.attribute.key for link in links})

    async with AsyncClient(
        url=meili_settings.url, api_key=meili_settings.key
    ) as client:
        search_service = MeilisearchService(client)
        listing_search_service = ListingSearchService(search_service)
        await listing_search_service.sync_schema(dynamic_filterable)

    await engine.dispose()
    print("✅ Search schema synced")


if __name__ == "__main__":
    asyncio.run(main())
