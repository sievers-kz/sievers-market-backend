from abc import ABC, abstractmethod


class IReferenceUnitOfWork(ABC):
    @property
    @abstractmethod
    def brand(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def color(self):
        raise NotImplementedError
