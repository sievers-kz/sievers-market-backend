from abc import ABC, abstractmethod

from src.core.customer.domain.enums import Kind
from src.core.customer.presentation.dto import TaxpayerResponse


class ITaxpayerGateway(ABC):
    @abstractmethod
    async def fetch(self, kind: Kind, tax_id: str) -> TaxpayerResponse | None:
        raise NotImplementedError
