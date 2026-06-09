import uuid

import pytest
import pytest_asyncio
from sqlalchemy import text

from src.core.listing.domain.entities import Listing
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.value_objects import Gallery, Image
from src.core.listing.presentation.dto import CreateListingRequest, ListingImage
from src.core.shared.domain.enums import PriceCurrency
from tests.iam.conftest import create_domain_account
from tests.vendor.conftest import create_domain_vendor


def create_domain_listing(owner_id: uuid.UUID, city_id: uuid.UUID, category_id: uuid.UUID, subcategory_id: uuid.UUID) -> Listing:
    return Listing(
        id=uuid.uuid4(),
        owner_id=owner_id,
        category_id=category_id,
        subcategory_id=subcategory_id,
        title="Трактор John Deere",
        price=5000000,
        currency=PriceCurrency.KZT,
        city_id=city_id,
        description="Тестовое описание",
        attributes={"engine_power": 300},
        gallery=Gallery(images=(
            Image(
                media_id=uuid.uuid4(),
                media_type="image/jpeg",
                media_size=1 * 1024 * 1024,
            ),
        )),
        status=ListingStatus.ACTIVE,
    )


@pytest_asyncio.fixture
async def create_listing_request(database_session):
    city_id = (await database_session.execute(text("SELECT id FROM cities LIMIT 1"))).scalar_one()
    category_id = (await database_session.execute(text("SELECT id FROM categories LIMIT 1"))).scalar_one()
    subcategory_id = (await database_session.execute(text("SELECT id FROM subcategories LIMIT 1"))).scalar_one()

    return CreateListingRequest(
        category_id=category_id,
        subcategory_id=subcategory_id,
        title="Трактор John Deere",
        price=5000000,
        currency=PriceCurrency.KZT,
        city_id=city_id,
        description="Тестовое описание",
        gallery=[ListingImage(
            media_id=uuid.uuid4(),
            media_type="image/jpeg",
            media_size=1 * 1024 * 1024,
        )],
        attributes={
            "engine_power": 300,
        },
    )


@pytest.fixture
def create_listing_usecase(container):
    return container.listing.create_listing_usecase()


@pytest.fixture
def activate_listing_usecase(container):
    return container.listing.activate_listing_usecase()


@pytest.fixture
def archive_listing_usecase(container):
    return container.listing.archive_listing_usecase()


@pytest.fixture
def deactivate_listing_usecase(container):
    return container.listing.deactivate_listing_usecase()


@pytest.fixture
def delete_listing_usecase(container):
    return container.listing.delete_listing_usecase()


@pytest.fixture
def change_listing_price_usecase(container):
    return container.listing.change_listing_price_usecase()


@pytest.fixture
def change_listing_location_usecase(container):
    return container.listing.change_listing_location_usecase()


@pytest.fixture
def change_listing_description_usecase(container):
    return container.listing.change_listing_description_usecase()


@pytest.fixture
def change_listing_attribute_usecase(container):
    return container.listing.change_listing_attribute_usecase()


@pytest_asyncio.fixture
async def listing_repository(container):
    return await container.listing.listing_repository()


@pytest_asyncio.fixture
async def create_listing(listing_repository, account_repository, vendor_repository, database_session):
    account = create_domain_account(is_active=True)
    await account_repository.save(account)

    vendor = create_domain_vendor(account_id=account.id)
    await vendor_repository.save(vendor)

    from sqlalchemy import text
    city_id = (await database_session.execute(text("SELECT id FROM cities LIMIT 1"))).scalar_one()
    category_id = (await database_session.execute(text("SELECT id FROM categories LIMIT 1"))).scalar_one()
    subcategory_id = (await database_session.execute(text("SELECT id FROM subcategories LIMIT 1"))).scalar_one()

    listing = create_domain_listing(
        owner_id=vendor.id,
        city_id=city_id,
        category_id=category_id,
        subcategory_id=subcategory_id,
    )

    await listing_repository.save(listing)
    return listing
