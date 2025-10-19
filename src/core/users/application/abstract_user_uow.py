from abc import abstractmethod

from src.core.shared.application.abstract_uow import AbstractUnitOfWork


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def user(self):
        raise NotImplementedError



