import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.domain.entities import Listing
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.value_objects import Gallery, Image
from src.core.shared.domain.enums import PriceCurrency


def make_listing(status: ListingStatus = ListingStatus.ACTIVE) -> Listing:
    return Listing(
        id=uuid.uuid4(),
        organization_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        subcategory_id=uuid.uuid4(),
        title="Трактор John Deere",
        price=5000000,
        currency=PriceCurrency.KZT,
        city_id=uuid.uuid4(),
        description="Тестовое описание",
        attributes={"brand": "John Deere", "condition": "used", "engine_power": 300},
        gallery=Gallery(images=(Image(media_id=uuid.uuid4(), media_type="image/jpeg", media_size=1024),)),
        status=status,
        created_at=datetime(2026, 11, 18, tzinfo=timezone.utc),
    )


@pytest.fixture
def meilisearch() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def catalog() -> AsyncMock:
    catalog = AsyncMock()
    catalog.get_filterable_keys.return_value = {"brand", "condition"}
    return catalog


@pytest.fixture
def service(meilisearch, catalog) -> ListingSearchService:
    return ListingSearchService(search_service=meilisearch, catalog_service=catalog)


class TestSyncListing:

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_active_listing_indexed_with_filterable_attributes_only(self, service, meilisearch, catalog):
        listing = make_listing()

        await service.sync_listing(listing)

        catalog.get_filterable_keys.assert_awaited_once_with(listing.subcategory_id)
        document = meilisearch.index_documents.await_args.kwargs["documents"][0]
        assert document["brand"] == "John Deere"
        assert document["condition"] == "used"
        assert "engine_power" not in document
        meilisearch.delete_documents.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_document_has_description_and_created_at(self, service, meilisearch):
        listing = make_listing()

        await service.sync_listing(listing)

        document = meilisearch.index_documents.await_args.kwargs["documents"][0]
        assert document["description"] == "Тестовое описание"
        assert document["created_at"] == int(listing.created_at.timestamp())
        assert document["is_active"] is True

    @pytest.mark.asyncio
    @pytest.mark.unit
    @pytest.mark.parametrize(
        "status",
        [ListingStatus.INACTIVE, ListingStatus.ARCHIVED, ListingStatus.DELETED],
    )
    async def test_not_active_listing_removed_from_index(self, service, meilisearch, catalog, status):
        listing = make_listing(status)

        await service.sync_listing(listing)

        meilisearch.delete_documents.assert_awaited_once_with(index_name="listing", document_ids=[str(listing.id)])
        meilisearch.index_documents.assert_not_awaited()
        catalog.get_filterable_keys.assert_not_awaited()
