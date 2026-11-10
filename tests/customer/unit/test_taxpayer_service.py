from unittest.mock import AsyncMock

import pytest

from src.core.customer.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.customer.application.services.taxpayer_service import TaxpayerService
from src.core.customer.domain.enums import Kind
from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError
from tests.customer.conftest import create_taxpayer

TAX_ID = "180240041089"


@pytest.fixture
def gateway():
    return AsyncMock(spec=ITaxpayerGateway)


@pytest.fixture
def service(gateway):
    return TaxpayerService(gateway=gateway)


class TestTaxpayerService:
    @pytest.mark.unit
    async def test_returns_taxpayer_when_found_active_and_kind_matches(self, service, gateway):
        taxpayer = create_taxpayer(TAX_ID, kind=Kind.COMPANY)
        gateway.fetch.return_value = taxpayer

        result = await service.verify(Kind.COMPANY, TAX_ID)

        assert result == taxpayer
        gateway.fetch.assert_awaited_once_with(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    async def test_returns_none_when_registry_has_no_record(self, service, gateway):
        gateway.fetch.return_value = None

        assert await service.verify(Kind.COMPANY, TAX_ID) is None

    @pytest.mark.unit
    async def test_returns_none_when_kind_does_not_match(self, service, gateway):
        # DaData finds by number only; the user said "individual" for a company BIN.
        gateway.fetch.return_value = create_taxpayer(TAX_ID, kind=Kind.COMPANY)

        assert await service.verify(Kind.INDIVIDUAL, TAX_ID) is None

    @pytest.mark.unit
    async def test_returns_none_when_taxpayer_is_inactive(self, service, gateway):
        gateway.fetch.return_value = create_taxpayer(TAX_ID, is_active=False)

        assert await service.verify(Kind.COMPANY, TAX_ID) is None

    @pytest.mark.unit
    async def test_propagates_registry_unavailable(self, service, gateway):
        gateway.fetch.side_effect = TaxpayerRegistryUnavailableError()

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await service.verify(Kind.COMPANY, TAX_ID)
