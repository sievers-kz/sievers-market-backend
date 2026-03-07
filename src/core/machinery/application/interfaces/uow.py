from abc import ABC, abstractmethod

from src.core.machinery.application.interfaces.repository import IMachineryRepository


class IMachineryUnitOfWork(ABC):
    @property
    @abstractmethod
    def machinery(self) -> IMachineryRepository:
        raise NotImplementedError
