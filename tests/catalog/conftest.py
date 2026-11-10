import pytest
import pytest_asyncio
from sqlalchemy import text

from tests.listing.conftest import create_domain_listing


@pytest.fixture
def catalog_query_service(container):
    return container.catalog.query_service()


@pytest_asyncio.fixture
async def created_listing(create_organization, listing_repository, database_session):
    city_id = (await database_session.execute(text("SELECT id FROM cities ORDER BY created_at LIMIT 1"))).scalar_one()
    category_id = (
        await database_session.execute(text("SELECT id FROM categories ORDER BY created_at LIMIT 1"))
    ).scalar_one()
    subcategory_id = (
        await database_session.execute(text("SELECT id FROM subcategories ORDER BY created_at LIMIT 1"))
    ).scalar_one()

    listing = create_domain_listing(
        organization_id=create_organization.id,
        city_id=city_id,
        category_id=category_id,
        subcategory_id=subcategory_id,
    )
    await listing_repository.save(listing)
    return listing, category_id, subcategory_id
