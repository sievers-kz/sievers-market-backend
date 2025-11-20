import uuid
from abc import ABC, abstractmethod

from src.core.users.domain.entities import User


class AbstractRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> User:
        pass

    @abstractmethod
    async def save(self, user: "") -> None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass
