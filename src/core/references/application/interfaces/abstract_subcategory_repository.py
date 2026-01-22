from abc import abstractmethod, ABC
from uuid import UUID


class AbstractSubcategoryRepository(ABC):
    @abstractmethod
    async def get_rubric_by_subcategory(self, subcategory_id: UUID):
        raise NotImplementedError
