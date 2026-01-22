from abc import ABC, abstractmethod

from src.core.machinery.application.interfaces.abstract_machinery_repository import AbstractMachineryRepository


class AbstractMachineryUnitOfWork(ABC):
    @property
    @abstractmethod
    def machinery(self) -> AbstractMachineryRepository:
        raise NotImplementedError
    