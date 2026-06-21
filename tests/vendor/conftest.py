import uuid

import pytest
import pytest_asyncio

from src.core.vendor.domain.entities import Vendor
from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.presentation.dto import CreateVendorRequest
from tests.iam.conftest import create_domain_account


def create_vendor_request():
    return CreateVendorRequest(
        contact_last_name="Testov",
        contact_first_name="Test",
        legal_name="Индивидуальный предприниматель AGROW",
        legal_address="Астана г. улица Тестова, дом №9, офис 03",
        tax_id="020716550967",
        legal_form=LegalForm.IE,
    )


@pytest.fixture
def mock_taxpayer_gateway(container):
    return container.vendor.mock_taxpayer_gateway()


@pytest.fixture
def taxpayer_validation_service(container, mock_taxpayer_gateway):
    container.vendor.kgd_taxpayer_gateway.override(mock_taxpayer_gateway)
    service = container.vendor.taxpayer_validation_service()

    yield service
    container.vendor.kgd_taxpayer_gateway.reset_override()


@pytest.fixture
def register_vendor_usecase(container):
    return container.vendor.register_vendor_usecase()


@pytest.fixture
def change_contact_fullname_usecase(container):
    return container.vendor.change_contact_fullname_usecase()


@pytest.fixture
def change_contact_phone_usecase(container):
    return container.vendor.change_contact_phone_usecase()


@pytest.fixture
def change_shop_name_usecase(container):
    return container.vendor.change_shop_name_usecase()


@pytest.fixture
def change_logotype_usecase(container):
    return container.vendor.change_logotype_usecase()


@pytest.fixture
def close_vendor_usecase(container):
    return container.vendor.close_vendor_usecase()


@pytest.fixture
def restore_vendor_usecase(container):
    return container.vendor.restore_vendor_usecase()


@pytest_asyncio.fixture
async def vendor_repository(container):
    return await container.vendor.vendor_repository()


def create_domain_vendor(account_id=None) -> Vendor:
    return Vendor.create(
        account_id=account_id or uuid.uuid4(),
        contact_last_name="Иванов",
        contact_first_name="Иван",
        legal_name="ТОО Тест",
        legal_address="г. Астана",
        tax_id="180240041089",
        legal_form=LegalForm.LLP,
    )


@pytest_asyncio.fixture
async def create_vendor(vendor_repository, account_repository):
    account = create_domain_account(is_active=True)
    await account_repository.save(account)

    vendor = create_domain_vendor(account_id=account.id)
    await vendor_repository.save(vendor)
    return vendor
