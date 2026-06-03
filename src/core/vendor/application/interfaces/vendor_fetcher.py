from abc import ABC, abstractmethod
from typing import Optional

from src.core.vendor.presentation.dto import VendorValidationResponse


class IVendorFetcher(ABC):
    @abstractmethod
    async def fetch(self, tax_id: str) -> Optional[VendorValidationResponse]:
        raise NotImplementedError





