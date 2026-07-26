from uuid import uuid4

import pytest
from sqlalchemy import text


class TestCatalogQueryService:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_category_tree_success(self, catalog_query_service):
        result = await catalog_query_service.get_category_tree()

        assert result is not None
        assert len(result) > 0
        assert result[0].name is not None
        assert len(result[0].categories) > 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_subcategory_attributes_success(
        self, catalog_query_service, database_session
    ):
        subcategory_id = (
            await database_session.execute(
                text("SELECT id FROM subcategories ORDER BY created_at LIMIT 1")
            )
        ).scalar_one()

        result = await catalog_query_service.get_subcategory_attributes(subcategory_id)

        assert result is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_listings_card_success(
        self, catalog_query_service, created_listing
    ):
        listing, vendor, category_id, subcategory_id = created_listing

        result = await catalog_query_service.get_listings_card(
            category_id=category_id,
            subcategory_id=None,
            page=1,
            limit=20,
        )

        assert result["total"] >= 1
        assert len(result["items"]) >= 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_listings_card_with_subcategory_filter(
        self, catalog_query_service, created_listing
    ):
        listing, vendor, category_id, subcategory_id = created_listing

        result = await catalog_query_service.get_listings_card(
            category_id=category_id,
            subcategory_id=subcategory_id,
            page=1,
            limit=20,
        )

        assert result["total"] >= 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_listings_card_empty_for_unknown_category(
        self, catalog_query_service
    ):
        result = await catalog_query_service.get_listings_card(
            category_id=uuid4(),
            subcategory_id=None,
            page=1,
            limit=20,
        )

        assert result["total"] == 0
        assert result["items"] == []

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_listing_details_success(
        self, catalog_query_service, created_listing
    ):
        listing, vendor, category_id, subcategory_id = created_listing

        result = await catalog_query_service.get_listing_details(listing.id)

        assert result is not None
        assert result.id == listing.id
        assert result.title == listing.title
        assert result.price == listing.price

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_listing_details_returns_none_for_unknown(
        self, catalog_query_service
    ):
        result = await catalog_query_service.get_listing_details(uuid4())
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_vendors_card_success(
        self, catalog_query_service, created_listing
    ):
        result = await catalog_query_service.get_vendors_card(page=1, limit=20)

        assert result["total"] >= 1
        assert len(result["items"]) >= 1
        assert result["items"][0].is_verified is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_vendor_details_success(
        self, catalog_query_service, created_listing
    ):
        listing, vendor, category_id, subcategory_id = created_listing

        result = await catalog_query_service.get_vendor_details(vendor.id)

        assert result is not None
        assert result.id == vendor.id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_vendor_details_returns_none_for_unknown(
        self, catalog_query_service
    ):
        result = await catalog_query_service.get_vendor_details(uuid4())
        assert result is None
