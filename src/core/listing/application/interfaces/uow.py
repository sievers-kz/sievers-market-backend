from abc import ABC, abstractmethod

from src.core.listing.application.interfaces.repository import IListingRepository


class IListingUnitOfWork(ABC):
    @property
    @abstractmethod
    def listing(self) -> IListingRepository:
        raise NotImplementedError
