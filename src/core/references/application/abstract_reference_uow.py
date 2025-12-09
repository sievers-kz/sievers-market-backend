from abc import abstractmethod

from src.core.shared.application.abstract_uow import AbstractUnitOfWork


class AbstractReferenceUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def reference(self):
        raise NotImplementedError

