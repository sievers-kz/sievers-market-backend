from abc import ABC, abstractmethod


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def _connect(self):
        raise NotImplementedError

    @abstractmethod
    async def _close(self):
        raise NotImplementedError

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                await self.rollback()
        finally:
            await self._close()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class AbstractUserIdentityUnitOfWork(AbstractUnitOfWork):

    @property
    @abstractmethod
    def user(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def identity(self):
        raise NotImplementedError
