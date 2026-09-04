from abc import ABC, abstractmethod

from src.core.admin.application.interfaces.repository import IAdminRepository


class IAdminUnitOfWork(ABC):
    @property
    @abstractmethod
    def admin(self) -> IAdminRepository:
        raise NotImplementedError
