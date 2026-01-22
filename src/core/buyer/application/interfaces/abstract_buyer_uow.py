from abc import ABC, abstractmethod

from src.core.buyer.application.interfaces.abstract_buyer_repository import AbstractBuyerRepository


class AbstractBuyerUnitOfWork(ABC):
    @property
    @abstractmethod
    def buyer(self) -> AbstractBuyerRepository:
        raise NotImplementedError
