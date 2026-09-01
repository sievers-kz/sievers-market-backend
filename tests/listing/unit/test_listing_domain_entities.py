import uuid

import pytest

from src.core.listing.domain.entities import Listing
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.exceptions import (
    ListingActivationError,
    ListingArchivingError,
)
from src.core.listing.domain.value_objects import Gallery, Image
from src.core.shared.domain.enums import PriceCurrency


def create_listing(status=ListingStatus.ACTIVE) -> Listing:
    return Listing(
        id=uuid.uuid4(),
        owner_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        subcategory_id=uuid.uuid4(),
        title="Трактор John Deere",
        price=5000000,
        currency=PriceCurrency.KZT,
        city_id=uuid.uuid4(),
        description="Описание",
        attributes={},
        gallery=Gallery(
            images=(
                Image(
                    media_id=uuid.uuid4(),
                    media_type="image/jpeg",
                    media_size=1 * 1024 * 1024,
                ),
            )
        ),
        status=status,
    )


class TestListingEntity:

    @pytest.mark.unit
    def test_activate_from_inactive_success(self):
        listing = create_listing(status=ListingStatus.INACTIVE)
        listing.activate()
        assert listing.status == ListingStatus.ACTIVE

    @pytest.mark.unit
    def test_activate_already_active_no_error(self):
        listing = create_listing(status=ListingStatus.ACTIVE)
        listing.activate()
        assert listing.status == ListingStatus.ACTIVE

    @pytest.mark.unit
    def test_activate_deleted_raises(self):
        listing = create_listing(status=ListingStatus.DELETED)
        with pytest.raises(ListingActivationError):
            listing.activate()

    @pytest.mark.unit
    def test_deactivate_success(self):
        listing = create_listing(status=ListingStatus.ACTIVE)
        listing.deactivate()
        assert listing.status == ListingStatus.INACTIVE

    @pytest.mark.unit
    def test_deactivate_already_inactive_no_error(self):
        listing = create_listing(status=ListingStatus.INACTIVE)
        listing.deactivate()
        assert listing.status == ListingStatus.INACTIVE

    @pytest.mark.unit
    def test_archive_success(self):
        listing = create_listing(status=ListingStatus.ACTIVE)
        listing.archive()
        assert listing.status == ListingStatus.ARCHIVED

    @pytest.mark.unit
    def test_archive_already_archived_no_error(self):
        listing = create_listing(status=ListingStatus.ARCHIVED)
        listing.archive()
        assert listing.status == ListingStatus.ARCHIVED

    @pytest.mark.unit
    def test_archive_deleted_raises(self):
        listing = create_listing(status=ListingStatus.DELETED)
        with pytest.raises(ListingArchivingError):
            listing.archive()

    @pytest.mark.unit
    def test_delete_success(self):
        listing = create_listing(status=ListingStatus.ACTIVE)
        listing.delete()
        assert listing.status == ListingStatus.DELETED

    @pytest.mark.unit
    def test_delete_already_deleted_no_error(self):
        listing = create_listing(status=ListingStatus.DELETED)
        listing.delete()
        assert listing.status == ListingStatus.DELETED

    @pytest.mark.unit
    def test_change_price_success(self):
        listing = create_listing()
        listing.change_price(9000000, PriceCurrency.USD)
        assert listing.price == 9000000
        assert listing.currency == PriceCurrency.USD

    @pytest.mark.unit
    def test_change_location_success(self):
        listing = create_listing()
        new_city_id = uuid.uuid4()
        listing.change_location(new_city_id)
        assert listing.city_id == new_city_id

    @pytest.mark.unit
    def test_change_description_success(self):
        listing = create_listing()
        listing.change_description("Новое описание")
        assert listing.description == "Новое описание"

    @pytest.mark.unit
    def test_change_attributes_success(self):
        listing = create_listing()
        new_attrs = {"engine_power": 300, "fuel_type": "diesel"}
        listing.change_attributes(new_attrs)
        assert listing.attributes == new_attrs
