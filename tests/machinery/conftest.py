import uuid
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import select

from src.core.machinery.domain.entities import Machinery
from src.core.machinery.domain.enums import MachineryCondition
from src.core.machinery.domain.value_objects import Description, Title, Price, YearOfIssue
from src.core.machinery.presentation.dto import CreateMachineryRequest
from src.core.machinery.presentation.filters import MachineryFilter, MachineryOwnerFilter
from src.core.references.infrastructure.models import Subcategory, City, Brand, Color, Country
from src.core.shared.domain.enums import PriceCurrency, ListingStatus


def create_domain_machinery(
    customer_id: UUID | None = None,
    subcategory_id: UUID | None = None,
    city_id: UUID | None = None,
    brand_id: UUID | None = None,
    color_id: UUID | None = None,
    country_id: UUID | None = None,
    status: ListingStatus = ListingStatus.ACTIVE
):
    return Machinery(
        id=uuid.uuid4(),
        customer_id=customer_id or uuid.uuid4(),
        subcategory_id=subcategory_id or uuid.uuid4(),
        title=Title("John Deere 8000R"),
        price=Price(12000000),
        currency=PriceCurrency.KZT,
        city_id=city_id or uuid.uuid4(),
        description=Description("Test machinery description"),
        brand_id=brand_id or uuid.uuid4(),
        model="8000R",
        year_of_issue=YearOfIssue(2020),
        condition=MachineryCondition.NEW,
        color_id=color_id,
        country_id=country_id,
        attributes={"engine_power": 123},
        status=status,
    )


@pytest_asyncio.fixture
async def create_machinery_request(database_session):
    subcategory = (await database_session.execute(select(Subcategory).limit(1))).scalar()
    city = (await database_session.execute(select(City).limit(1))).scalar()
    brand = (await database_session.execute(select(Brand).limit(1))).scalar()

    return CreateMachineryRequest(
        subcategory_id=subcategory.id,
        price=12000000,
        currency=PriceCurrency.KZT,
        city_id=city.id,
        description="Test machinery description",
        brand_id=brand.id,
        model="8000R",
        year_of_issue=2020,
        condition=MachineryCondition.NEW,
        attributes={
            "engine_power": 123
        }
    )


@pytest.fixture
def default_filter():
    return MachineryFilter()


@pytest.fixture
def default_owner_filter():
    return MachineryOwnerFilter()


@pytest_asyncio.fixture
async def ref_ids(database_session):
    subcategory = (await database_session.execute(select(Subcategory).limit(1))).scalar()
    city = (await database_session.execute(select(City).limit(1))).scalar()
    brand = (await database_session.execute(select(Brand).limit(1))).scalar()
    color = (await database_session.execute(select(Color).limit(1))).scalar()
    country = (await database_session.execute(select(Country).limit(1))).scalar()

    return {
        "subcategory_id": subcategory.id,
        "city_id": city.id,
        "brand_id": brand.id,
        "color_id": color.id,
        "country_id": country.id,
    }


@pytest_asyncio.fixture
async def create_machinery_usecase(container):
    return await container.machinery.create_machinery_usecase()


@pytest_asyncio.fixture
async def machinery_repository(container):
    return await container.machinery.machinery_repository()


@pytest_asyncio.fixture
async def activate_machinery_usecase(container):
    return await container.machinery.activate_machinery_usecase()


@pytest_asyncio.fixture
async def deactivate_machinery_usecase(container):
    return await container.machinery.deactivate_machinery_usecase()


@pytest_asyncio.fixture
async def archive_machinery_usecase(container):
    return await container.machinery.archive_machinery_usecase()


@pytest_asyncio.fixture
async def delete_machinery_usecase(container):
    return await container.machinery.delete_machinery_usecase()


@pytest_asyncio.fixture
async def change_machinery_description_usecase(container):
    return await container.machinery.change_machinery_description_usecase()


@pytest_asyncio.fixture
async def change_machinery_general_usecase(container):
    return await container.machinery.change_machinery_general_usecase()


@pytest_asyncio.fixture
async def change_machinery_price_usecase(container):
    return await container.machinery.change_machinery_price_usecase()


@pytest_asyncio.fixture
async def change_machinery_operating_history_usecase(container):
    return await container.machinery.change_operating_history_usecase()


@pytest_asyncio.fixture
async def change_machinery_spec_usecase(container):
    return await container.machinery.change_machinery_spec_usecase()


@pytest_asyncio.fixture
async def get_customer_machinery_detail_usecase(container):
    return await container.machinery.get_customer_machinery_detail_usecase()


@pytest_asyncio.fixture
async def machinery_query_service(container):
    return await container.machinery.machinery_query()
