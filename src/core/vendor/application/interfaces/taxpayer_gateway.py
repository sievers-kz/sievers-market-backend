from abc import ABC, abstractmethod
from typing import Optional

from src.core.vendor.presentation.dto import TaxpayerResponse


class ITaxpayerGateway(ABC):
    @abstractmethod
    async def fetch(self, tax_id: str) -> Optional[TaxpayerResponse]:
        raise NotImplementedError
