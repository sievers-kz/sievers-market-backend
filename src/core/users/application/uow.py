from abc import ABC, abstractmethod
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractUnitOfWork(ABC):
    @abstractmethod
    async def _connect(self):
        raise NotImplementedError

    @abstractmethod
    async def _close(self):
        raise NotImplementedError

    async def __aenter__(self):
        if not self._connect():
            raise RuntimeError("Session unavailable")

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


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    @property
    @abstractmethod
    def user(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def token(self):
        raise NotImplementedError


