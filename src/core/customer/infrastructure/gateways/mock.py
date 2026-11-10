from src.core.customer.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.customer.domain.enums import Kind
from src.core.customer.presentation.dto import TaxpayerResponse

KIND_TAXPAYER_TYPE_MAP = {Kind.INDIVIDUAL: "IP", Kind.COMPANY: "UL"}


class MockTaxpayerGateway(ITaxpayerGateway):
    def __init__(self):
        self._taxpayers_database = {
            "020716550967": {
                "name": "Индивидуальный предприниматель AGROW",
                "type": "IP",
                "is_liquidation": False,
            },
            "180240041089": {
                "name": "Товарищество с ограниченной ответственностью Olzha Agro",
                "type": "UL",
                "is_liquidation": False,
            },
            "050540005822": {
                "name": "Товарищество с ограниченной ответственностью Родина",
                "type": "UL",
                "is_liquidation": True,
            },
        }

    async def fetch(self, kind: Kind, tax_id: str) -> TaxpayerResponse | None:
        taxpayer = self._taxpayers_database.get(tax_id)
        if not taxpayer or taxpayer["type"] != KIND_TAXPAYER_TYPE_MAP[kind]:
            return None

        return TaxpayerResponse(
            tax_id=tax_id,
            legal_name=taxpayer["name"],
            kind=kind,
            is_active=not taxpayer["is_liquidation"],
        )
