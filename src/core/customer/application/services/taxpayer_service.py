from src.core.customer.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.customer.domain.enums import Kind
from src.core.customer.presentation.dto import TaxpayerResponse


class TaxpayerService:
    def __init__(self, gateway: ITaxpayerGateway) -> None:
        self.gateway = gateway

    async def verify(self, kind: Kind, tax_id: str) -> TaxpayerResponse | None:
        taxpayer = await self.gateway.fetch(kind, tax_id)
        if taxpayer is None or taxpayer.kind != kind or not taxpayer.is_active:
            return None

        return taxpayer
