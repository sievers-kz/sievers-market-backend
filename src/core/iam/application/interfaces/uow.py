from abc import ABC, abstractmethod


class IIAMUnitOfWork(ABC):
    @property
    @abstractmethod
    def account(self):
        raise NotImplementedError
