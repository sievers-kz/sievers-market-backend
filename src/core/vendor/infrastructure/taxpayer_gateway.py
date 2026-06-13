from typing import Optional

from src.core.vendor.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.presentation.dto import TaxpayerResponse


class MockTaxpayerGateway(ITaxpayerGateway):
    def __init__(self):
        self._taxpayers_database = {
            "020716550967": {
                "name": "Индивидуальный предприниматель AGROW",
                "address": "г. Астана, проспект Бауыржан Момышулы, д. 9",
                "type": LegalForm.IE,
                "is_liquidation": False,
            },
            "180240041089": {
                "name": "Товарищество с ограниченной ответственностью Olzha Agro",
                "address": "г. Костанай, проспект Нұрсұлтан Назарбаев, д. 170",
                "type": LegalForm.LLP,
                "is_liquidation": False,
            },
            "050540005822": {
                "name": "Товарищество с ограниченной ответственностью Родина",
                "address": "Целиноградский район, село Родина, улица Центральная, строение 15",  # noqa: E501
                "type": LegalForm.LLP,
                "is_liquidation": True,
            },
        }

    async def fetch(self, tax_id: str) -> Optional[TaxpayerResponse]:
        taxpayer = self._taxpayers_database.get(tax_id)
        if not taxpayer:
            return None

        return TaxpayerResponse(
            tax_id=tax_id,
            legal_name=taxpayer["name"],
            legal_address=taxpayer["address"],
            legal_form=taxpayer["type"],
            is_liquidation=taxpayer["is_liquidation"],
        )


class RealTaxpayerGateway(ITaxpayerGateway):
    def __init__(self):
        self._taxpayers_database = {}

    async def fetch(self, tax_id: str) -> Optional[TaxpayerResponse]:
        pass
