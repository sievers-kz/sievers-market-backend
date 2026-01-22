from abc import ABC, abstractmethod


class AbstractColorRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
