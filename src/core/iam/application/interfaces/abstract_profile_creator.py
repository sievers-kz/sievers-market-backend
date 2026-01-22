from abc import ABC, abstractmethod
from uuid import UUID


class AbstractProfileCreator(ABC):
    @abstractmethod
    async def create(self, account_id: UUID, profile_data):
        raise NotImplementedError
