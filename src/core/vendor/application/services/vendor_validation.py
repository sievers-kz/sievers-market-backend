from typing import Optional

from src.core.vendor.application.interfaces.vendor_fetcher import IVendorFetcher
from src.core.vendor.domain.exceptions import VendorNotFoundError, VendorOnLiquidationError
from src.core.vendor.presentation.dto import VendorValidationResponse


class VendorValidationService:
    def __init__(self, fetcher: IVendorFetcher):
        self._fetcher = fetcher

    async def verify(self, tax_id: str) -> Optional[VendorValidationResponse]:
        vendor = await self._fetcher.fetch(tax_id)
        if not vendor:
            raise VendorNotFoundError()
        if vendor.is_liquidation:
            raise VendorOnLiquidationError()
        return vendor
