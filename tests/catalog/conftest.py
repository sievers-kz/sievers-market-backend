import pytest_asyncio
from sqlalchemy import text

from tests.iam.conftest import create_domain_account
from tests.listing.conftest import create_domain_listing
from tests.vendor.conftest import create_domain_vendor


@pytest_asyncio.fixture
async def catalog_query_service(container):
    return await container.catalog.query_service()


@pytest_asyncio.fixture
async def created_listing(
    account_repository, vendor_repository, listing_repository, database_session
):
    account = create_domain_account(is_active=True)
    await account_repository.save(account)

    vendor = create_domain_vendor(account_id=account.id)
    vendor.is_verified = True
    await vendor_repository.save(vendor)

    city_id = (
        await database_session.execute(
            text("SELECT id FROM cities ORDER BY created_at LIMIT 1")
        )
    ).scalar_one()
    category_id = (
        await database_session.execute(
            text("SELECT id FROM categories ORDER BY created_at LIMIT 1")
        )
    ).scalar_one()
    subcategory_id = (
        await database_session.execute(
            text("SELECT id FROM subcategories ORDER BY created_at LIMIT 1")
        )
    ).scalar_one()

    listing = create_domain_listing(
        owner_id=vendor.id,
        city_id=city_id,
        category_id=category_id,
        subcategory_id=subcategory_id,
    )
    await listing_repository.save(listing)
    return listing, vendor, category_id, subcategory_id
