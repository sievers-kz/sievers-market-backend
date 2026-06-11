import uuid

import pytest
import pytest_asyncio

from src.core.customer.domain.entities import Customer
from src.core.customer.domain.value_objects import Fullname
from tests.iam.conftest import create_domain_account


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
    await customer_repository.save(customer)
    return customer


@pytest.fixture
def create_customer_usecase(container):
    return container.customer.create_customer_usecase()


@pytest.fixture
def change_customer_fullname_usecase(container):
    return container.customer.change_customer_fullname_usecase()


@pytest_asyncio.fixture
async def customer_repository(container):
    return await container.customer.customer_repository()





