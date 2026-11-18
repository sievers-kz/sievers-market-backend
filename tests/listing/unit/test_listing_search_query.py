import uuid
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError

from src.core.catalog.infrastructure.enums import AttributeType
from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.application.usecases import SearchListingsUseCase
from src.core.listing.domain.exceptions import (
    ListingAttributeFilterWithoutSubcategoryError,
    ListingInvalidFilterKeyError,
    ListingInvalidRangeFilterError,
)
from src.core.listing.presentation.dto import ListingSearchQuery, ListingSearchSort, NumericRange
from src.core.shared.presentation.dto import SearchResult


@pytest.fixture
def catalog() -> AsyncMock:
    catalog = AsyncMock()
    catalog.get_filterable_types.return_value = {
        "brand": AttributeType.REFERENCE,
        "condition": AttributeType.ENUMERATE,
        "year_of_issue": AttributeType.INTEGER,
    }
    return catalog


@pytest.fixture
def meilisearch() -> AsyncMock:
    meilisearch = AsyncMock()
    meilisearch.search.return_value = SearchResult(hits=[], total=0, page=1, pages=0)
    return meilisearch


@pytest.fixture
def service(meilisearch, catalog) -> ListingSearchService:
    return ListingSearchService(search_service=meilisearch, catalog_service=catalog)


class TestAttributeKeyValidation:

    @pytest.mark.unit
    async def test_attributes_without_subcategory_rejected(self, service, meilisearch):
        query = ListingSearchQuery(attributes={"brand": "John Deere"})

        with pytest.raises(ListingAttributeFilterWithoutSubcategoryError):
            await service.search_listings(query)
        meilisearch.search.assert_not_awaited()

    @pytest.mark.unit
    async def test_unknown_key_rejected(self, service, meilisearch):
        query = ListingSearchQuery(subcategory_id=uuid.uuid4(), attributes={"colour": "red"})

        with pytest.raises(ListingInvalidFilterKeyError):
            await service.search_listings(query)
        meilisearch.search.assert_not_awaited()

    @pytest.mark.unit
    async def test_filterable_key_passes_and_only_ids_requested(self, service, meilisearch, catalog):
        subcategory_id = uuid.uuid4()
        query = ListingSearchQuery(subcategory_id=subcategory_id, attributes={"brand": "John Deere"})

        await service.search_listings(query)

        catalog.get_filterable_types.assert_awaited_once_with(subcategory_id)
        kwargs = meilisearch.search.await_args.kwargs
        assert 'brand = "John Deere"' in kwargs["filter_expression"]
        assert kwargs["attributes_to_retrieve"] == ["id"]

    @pytest.mark.unit
    async def test_no_attributes_skips_catalog(self, service, catalog):
        await service.search_listings(ListingSearchQuery(text="трактор"))

        catalog.get_filterable_types.assert_not_awaited()


class TestAttributeRanges:

    @pytest.mark.unit
    async def test_range_on_numeric_attribute_builds_bounds(self, service, meilisearch):
        query = ListingSearchQuery(
            subcategory_id=uuid.uuid4(),
            attribute_ranges={"year_of_issue": {"min": 2015, "max": 2020}},
        )

        await service.search_listings(query)

        filters = meilisearch.search.await_args.kwargs["filter_expression"]
        assert "year_of_issue >= 2015.0" in filters
        assert "year_of_issue <= 2020.0" in filters

    @pytest.mark.unit
    async def test_single_bound(self, service, meilisearch):
        query = ListingSearchQuery(subcategory_id=uuid.uuid4(), attribute_ranges={"year_of_issue": {"min": 2015}})

        await service.search_listings(query)

        filters = meilisearch.search.await_args.kwargs["filter_expression"]
        assert "year_of_issue >= 2015.0" in filters
        assert not any(item.startswith("year_of_issue <=") for item in filters)

    @pytest.mark.unit
    async def test_range_on_non_numeric_attribute_rejected(self, service, meilisearch):
        query = ListingSearchQuery(subcategory_id=uuid.uuid4(), attribute_ranges={"condition": {"min": 1}})

        with pytest.raises(ListingInvalidRangeFilterError):
            await service.search_listings(query)
        meilisearch.search.assert_not_awaited()

    @pytest.mark.unit
    async def test_range_on_unknown_attribute_rejected(self, service):
        query = ListingSearchQuery(subcategory_id=uuid.uuid4(), attribute_ranges={"torque": {"min": 1}})

        with pytest.raises(ListingInvalidFilterKeyError):
            await service.search_listings(query)

    @pytest.mark.unit
    async def test_range_without_subcategory_rejected(self, service):
        query = ListingSearchQuery(attribute_ranges={"year_of_issue": {"min": 2015}})

        with pytest.raises(ListingAttributeFilterWithoutSubcategoryError):
            await service.search_listings(query)

    @pytest.mark.unit
    @pytest.mark.parametrize("bounds", [{}, {"min": 5, "max": 1}, {"min": float("inf")}])
    def test_invalid_bounds_rejected_by_dto(self, bounds):
        with pytest.raises(ValidationError):
            NumericRange(**bounds)


class TestPriceCurrency:

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "query",
        [
            ListingSearchQuery(price_min=1_000_000),
            ListingSearchQuery(price_max=5_000_000),
            ListingSearchQuery(sort=ListingSearchSort.PRICE_ASC),
            ListingSearchQuery(sort=ListingSearchSort.PRICE_DESC),
        ],
    )
    def test_price_filter_or_sort_limits_to_kzt(self, service, query):
        assert 'currency = "KZT"' in service.build_filter(query)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "query",
        [ListingSearchQuery(), ListingSearchQuery(sort=ListingSearchSort.NEWEST), ListingSearchQuery(text="трактор")],
    )
    def test_without_price_all_currencies(self, service, query):
        assert not any(item.startswith("currency") for item in service.build_filter(query))


class TestSort:

    @pytest.mark.unit
    def test_explicit_sort(self, service):
        assert service.build_sort(ListingSearchQuery(sort=ListingSearchSort.PRICE_ASC)) == ["price:asc"]
        assert service.build_sort(ListingSearchQuery(sort=ListingSearchSort.PRICE_DESC)) == ["price:desc"]

    @pytest.mark.unit
    def test_default_without_text_is_newest(self, service):
        assert service.build_sort(ListingSearchQuery()) == ["created_at:desc"]

    @pytest.mark.unit
    def test_default_with_text_is_relevance(self, service):
        assert service.build_sort(ListingSearchQuery(text="трактор")) is None

    @pytest.mark.unit
    def test_category_filter(self, service):
        category_id = uuid.uuid4()
        filters = service.build_filter(ListingSearchQuery(category_id=category_id))
        assert f'category_id = "{category_id}"' in filters


class TestSearchListingsUseCase:

    @pytest.mark.unit
    async def test_keeps_meilisearch_order_and_skips_missing(self):
        first, second, gone = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
        search = AsyncMock()
        search.search_listings.return_value = SearchResult(
            hits=[{"id": str(second)}, {"id": str(gone)}, {"id": str(first)}],
            total=3,
            page=1,
            pages=1,
        )
        query_service = AsyncMock()
        # Postgres отдаёт в своём порядке и без объявления, которое уже неактивно.
        query_service.get_listings_by_ids.return_value = [_card(first), _card(second)]
        usecase = SearchListingsUseCase(listing_search_service=search, query_service=query_service)

        result = await usecase.execute(ListingSearchQuery())

        assert [item.id for item in result.items] == [second, first]
        assert result.total == 3
        query_service.get_listings_by_ids.assert_awaited_once_with([second, gone, first])


def _card(listing_id):
    from src.core.listing.presentation.dto import ListingCardResponse

    return ListingCardResponse.model_construct(id=listing_id)
