from abc import ABC, abstractmethod

from src.core.customer.application.interfaces.repository import ICustomerRepository


class ICustomerUnitOfWork(ABC):
    @property
    @abstractmethod
    def customer(self) -> ICustomerRepository:
        raise NotImplementedError
