from abc import ABC, abstractmethod


class AbstractSellerUnitOfWork(ABC):
    @property
    @abstractmethod
    def seller(self):
        raise NotImplementedError
