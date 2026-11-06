from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.core.listing.application.services.listing_search import ListingSearchService
from src.core.listing.domain.exceptions import ListingInvalidFilterKeyError
from src.core.listing.presentation.dto import ListingSearchQuery


@pytest.fixture
def service() -> ListingSearchService:
    return ListingSearchService(search_service=MagicMock())


class TestBuildFilter:

    @pytest.mark.unit
    def test_only_active_by_default(self, service):
        assert service.build_filter(ListingSearchQuery()) == ["is_active = true"]

    @pytest.mark.unit
    def test_uuid_and_price_filters(self, service):
        subcategory_id, city_id = uuid4(), uuid4()
        query = ListingSearchQuery(
            subcategory_id=subcategory_id,
            city_id=city_id,
            price_min=100,
            price_max=500,
        )

        assert service.build_filter(query) == [
            "is_active = true",
            f'subcategory_id = "{subcategory_id}"',
            f'city_id = "{city_id}"',
            "price >= 100",
            "price <= 500",
        ]

    @pytest.mark.unit
    def test_attribute_values_by_type(self, service):
        query = ListingSearchQuery(attributes={"color": "red", "year": 2020, "volume": 1.5, "is_new": True})

        assert service.build_filter(query)[1:] == [
            'color = "red"',
            "year = 2020",
            "volume = 1.5",
            "is_new = true",
        ]

    @pytest.mark.unit
    def test_false_is_not_formatted_as_number(self, service):
        query = ListingSearchQuery(attributes={"is_new": False})

        assert service.build_filter(query)[1] == "is_new = false"

    @pytest.mark.unit
    def test_quote_in_value_is_escaped(self, service):
        query = ListingSearchQuery(attributes={"color": 'a" OR price > 0 OR "b'})

        assert service.build_filter(query)[1] == 'color = "a\\" OR price > 0 OR \\"b"'

    @pytest.mark.unit
    def test_trailing_backslash_cannot_escape_closing_quote(self, service):
        query = ListingSearchQuery(attributes={"color": "red\\"})

        assert service.build_filter(query)[1] == 'color = "red\\\\"'

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "key",
        [
            "color = 1 OR is_active",
            "x OR is_active = false",
            "Color",
            "1color",
            "",
            "a-b",
            'a"',
        ],
    )
    def test_invalid_attribute_key_is_rejected(self, service, key):
        query = ListingSearchQuery(attributes={key: "red"})

        with pytest.raises(ListingInvalidFilterKeyError):
            service.build_filter(query)


class TestListingSearchQuery:

    @pytest.mark.unit
    @pytest.mark.parametrize("field", ["subcategory_id", "city_id"])
    def test_not_uuid_is_rejected(self, field):
        with pytest.raises(ValidationError):
            ListingSearchQuery(**{field: 'x" OR is_active = false OR city_id = "'})

    @pytest.mark.unit
    @pytest.mark.parametrize("value", [{"nested": 1}, [1, 2], None])
    def test_attribute_value_must_be_scalar(self, value):
        with pytest.raises(ValidationError):
            ListingSearchQuery(attributes={"color": value})

    @pytest.mark.unit
    @pytest.mark.parametrize("value", [float("nan"), float("inf")])
    def test_non_finite_number_is_rejected(self, value):
        with pytest.raises(ValidationError):
            ListingSearchQuery(attributes={"volume": value})
