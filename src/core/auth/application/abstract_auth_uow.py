from abc import abstractmethod

from src.core.shared.application.abstract_uow import AbstractUnitOfWork


class AbstractAuthUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def token(self):
        raise NotImplementedError
