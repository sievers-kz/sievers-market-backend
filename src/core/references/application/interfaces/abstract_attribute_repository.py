from abc import abstractmethod, ABC
from uuid import UUID


class AbstractAttributeRepository(ABC):
    @abstractmethod
    async def get_by_subcategory_id(self, subcategory_id: UUID):
        raise NotImplementedError
