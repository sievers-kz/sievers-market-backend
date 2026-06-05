from abc import ABC, abstractmethod

from src.core.customer.application.interfaces.abstract_customer_repository import AbstractCustomerRepository


class AbstractCustomerUnitOfWork(ABC):
    @property
    @abstractmethod
    def customer(self) -> AbstractCustomerRepository:
        raise NotImplementedError
