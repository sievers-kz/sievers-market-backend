from abc import ABC, abstractmethod


class AbstractIAMUnitOfWork(ABC):
    @property
    @abstractmethod
    def account(self):
        raise NotImplementedError
