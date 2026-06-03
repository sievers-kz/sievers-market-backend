from abc import ABC, abstractmethod
from src.core.vendor.application.interfaces.repository import IVendorRepository


class IVendorUnitOfWork(ABC):
    @property
    @abstractmethod
    def vendor(self) -> IVendorRepository:
        raise NotImplementedError
