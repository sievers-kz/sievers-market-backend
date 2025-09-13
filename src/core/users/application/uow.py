from abc import ABC, abstractmethod
from typing import Callable, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractUnitOfWork(ABC):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self._session_factory = session_factory
        self.session: Optional[AsyncSession] = None
        self._entered = False

    async def __aenter__(self):
        if self._entered:
            raise RuntimeError("UoW already entered!")

        try:
            self.session = self._session_factory()
            self._entered = True
            return self
        except Exception as e:
            print(f"Error entering UoW: {e}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._entered:
            return

        try:
            if exc_type:
                await self.rollback()
        finally:
            await self._safe_close()
            self._entered = False

    async def _safe_close(self):
        if self.session:
            try:
                await self.session.close()
            except Exception as e:
                print(f"Error closing session: {e}")
            finally:
                self.session = None

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


