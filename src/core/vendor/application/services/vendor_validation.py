from typing import Optional

from src.core.vendor.application.interfaces.vendor_fetcher import IVendorFetcher
from src.core.vendor.presentation.dto import VendorValidationResponse


class VendorValidationService:
    def __init__(self, fetcher: IVendorFetcher):
        self._fetcher = fetcher

    async def verify(self, tax_id: str) -> Optional[VendorValidationResponse]:
        vendor = await self._fetcher.fetch(tax_id)
        if not vendor:
            raise ValueError(f"Не удалось найти компанию по ID: {tax_id}")
        if vendor.is_liquidation:
            raise ValueError("Данная компания находится на ликвидации")
        return vendor
