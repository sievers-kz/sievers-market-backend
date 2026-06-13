from typing import Optional

from src.core.shared.application.interfaces.cache_service import ICacheService
from src.core.vendor.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.vendor.domain.exceptions import (
    VendorNotFoundError,
    VendorOnLiquidationError,
)
from src.core.vendor.presentation.dto import TaxpayerResponse


class TaxpayerValidationService:
    def __init__(self, gateway: ITaxpayerGateway, cache_service: ICacheService):
        self.gateway = gateway
        self.cache_service = cache_service

    async def validate(self, tax_id: str) -> Optional[TaxpayerResponse]:
        taxpayer = await self.gateway.fetch(tax_id)
        if not taxpayer:
            raise VendorNotFoundError()

        if taxpayer.is_liquidation:
            raise VendorOnLiquidationError()

        await self.cache_service.set(
            key=f"taxpayer:{tax_id}", value=taxpayer.model_dump_json(), ttl=300
        )

        return taxpayer
