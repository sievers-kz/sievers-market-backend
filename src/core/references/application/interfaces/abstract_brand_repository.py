from abc import ABC, abstractmethod


class AbstractBrandRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, brand_id: int):
        raise NotImplementedError
