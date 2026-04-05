import uuid

import pytest_asyncio

from src.core.customer.domain.entities import Customer
from src.core.customer.domain.value_objects import Fullname
from tests.iam.conftest import create_domain_account


@pytest_asyncio.fixture
async def change_customer_fullname_usecase(container):
    return await container.customer.change_customer_fullname_usecase()


@pytest_asyncio.fixture
async def customer_repository(container):
    return await container.customer.customer_repository()


@pytest_asyncio.fixture
async def account_repository(container):
    return await container.iam.account_repository()


@pytest_asyncio.fixture
async def create_customer(customer_repository, account_repository):
    account = create_domain_account(is_active=True)
    await account_repository.save(account)

    customer = Customer(
        id=uuid.uuid4(),
        account_id=account.id,
        fullname=Fullname(
            first_name="Test",
            last_name="Test",
            patronymic="Test",
        ),
    )
    return customer

