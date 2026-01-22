from abc import ABC, abstractmethod


class AbstractBrandRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
