from typing import Optional

from src.core.vendor.application.interfaces.vendor_fetcher import IVendorFetcher
from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.presentation.dto import VendorValidationResponse


class MockVendorFetcher(IVendorFetcher):
    def __init__(self):
        self._vendors_database = {
            "020716550967": {
                "name": "Индивидуальный предприниматель AGROW",
                "type": LegalForm.IE,
                "is_liquidation": False,
            },
            "180240041089": {
                "name": "Товарищество с ограниченной ответственностью Olzha Agro",
                "type": LegalForm.LLP,
                "is_liquidation": False,
            },
            "050540005822": {
                "name": "Товарищество с ограниченной ответственностью Родина",
                "type": LegalForm.LLP,
                "is_liquidation": False,
            }
        }

    async def fetch(self, tax_id: str) -> Optional[VendorValidationResponse]:
        raw_vendor = self._vendors_database.get(tax_id)
        if not raw_vendor:
            return None

        return VendorValidationResponse(
            tax_id=tax_id,
            name=raw_vendor["name"],
            type=raw_vendor["type"],
            is_liquidation=raw_vendor["is_liquidation"],
        )



