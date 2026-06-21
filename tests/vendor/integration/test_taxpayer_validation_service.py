import pytest

from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.domain.exceptions import (
    VendorNotFoundError,
    VendorOnLiquidationError,
)
from src.core.vendor.presentation.dto import TaxpayerResponse


class TestTaxpayerValidationService:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_taxpayer_validation_response(
        self, taxpayer_validation_service
    ):
        tax_id = "020716550967"
        response = await taxpayer_validation_service.validate(tax_id, LegalForm.IE)

        assert response is not None
        assert response.tax_id == tax_id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_successful_save_taxpayer_in_redis(
        self, taxpayer_validation_service, redis_service
    ):
        tax_id = "020716550967"
        await taxpayer_validation_service.validate(tax_id, LegalForm.IE)

        cached_taxpayer = await redis_service.get(f"taxpayer:{tax_id}")
        taxpayer = TaxpayerResponse.model_validate_json(cached_taxpayer)

        assert taxpayer is not None
        assert taxpayer.tax_id == tax_id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_taxpayer_not_found_raises(
        self, taxpayer_validation_service, redis_service
    ):
        tax_id = "123456789012"
        with pytest.raises(VendorNotFoundError):
            await taxpayer_validation_service.validate(tax_id, LegalForm.LLP)

        cached_taxpayer = await redis_service.get(f"taxpayer:{tax_id}")
        assert cached_taxpayer is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_taxpayer_on_liquidation_raises(
        self, taxpayer_validation_service, redis_service
    ):
        tax_id = "050540005822"
        with pytest.raises(VendorOnLiquidationError):
            await taxpayer_validation_service.validate(tax_id, LegalForm.LLP)

        cached_taxpayer = await redis_service.get(f"taxpayer:{tax_id}")
        assert cached_taxpayer is None
