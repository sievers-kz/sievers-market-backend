import random
from dataclasses import replace
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from src.core.customer.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.customer.domain.entities import Customer, Organization
from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.customer.presentation.dto import TaxpayerResponse
from src.core.iam.domain.value_objects import Email
from tests.iam.conftest import create_domain_account


def random_tax_id() -> str:
    return "".join(random.choices("0123456789", k=12))


def create_domain_organization(
    owner_id,
    tax_id: str | None = None,
    kind: Kind = Kind.COMPANY,
    registry_status: RegistryStatus = RegistryStatus.PENDING,
) -> Organization:
    organization = Organization.create(owner_id=owner_id, tax_id=tax_id or random_tax_id(), kind=kind)
    organization.registry_status = registry_status
    return organization


def create_taxpayer(
    tax_id: str,
    kind: Kind = Kind.COMPANY,
    legal_name: str = 'ТОО "Тест Агро"',
    is_active: bool = True,
) -> TaxpayerResponse:
    return TaxpayerResponse(tax_id=tax_id, legal_name=legal_name, kind=kind, is_active=is_active)


@pytest.fixture
def customer_uow(container):
    return container.customer.uow()


@pytest_asyncio.fixture
async def make_customer(account_repository, customer_uow):
    """Creates an account plus a customer profile; pass a distinct email for every extra customer."""

    async def _make(email: str = "test@example.com") -> Customer:
        account = replace(create_domain_account(is_active=True), email=Email(email))
        await account_repository.save(account)

        customer = Customer.create(account_id=account.id)
        async with customer_uow as uow:
            await uow.customer.save(customer)
            await uow.commit()
        return customer

    return _make


@pytest_asyncio.fixture
async def create_customer(make_customer) -> Customer:
    return await make_customer()


@pytest_asyncio.fixture
async def other_customer(make_customer) -> Customer:
    return await make_customer("other@example.com")


@pytest_asyncio.fixture
async def save_organization(customer_uow):
    """Persists a prepared Organization aggregate and returns it."""

    async def _save(organization: Organization) -> Organization:
        async with customer_uow as uow:
            await uow.organization.save(organization)
            await uow.commit()
        return organization

    return _save


@pytest_asyncio.fixture
async def get_organization(customer_uow):
    async def _get(organization_id):
        async with customer_uow as uow:
            return await uow.organization.get_by_id(organization_id)

    return _get


@pytest_asyncio.fixture
async def create_organization(create_customer, save_organization) -> Organization:
    """A verified organization, ready to own listings."""
    organization = create_domain_organization(owner_id=create_customer.id, registry_status=RegistryStatus.VERIFIED)
    return await save_organization(organization)


@pytest.fixture
def mock_taxpayer_gateway(container):
    mock = AsyncMock(spec=ITaxpayerGateway)
    with container.customer.taxpayer_gateway.override(mock):
        yield mock


@pytest.fixture
def create_organization_usecase(container, mock_arq):
    return container.customer.create_organization_usecase()


@pytest.fixture
def delete_organization_usecase(container):
    return container.customer.delete_organization_usecase()


@pytest.fixture
def verify_organization_registry_usecase(container, mock_taxpayer_gateway):
    # No `await` here, unlike in the worker: tests override session_factory with a plain factory,
    # while in production it depends on the async engine Resource and the provider returns a Future.
    return container.customer.verify_organization_registry_usecase()


@pytest.fixture
def organization_service(container):
    return container.customer.organization_service()
