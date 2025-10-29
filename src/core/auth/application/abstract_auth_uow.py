from abc import abstractmethod

from src.core.shared.application.abstract_uow import AbstractUnitOfWork


class AbstractIdentityUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def identity(self):
        raise NotImplementedError

