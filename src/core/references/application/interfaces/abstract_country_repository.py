from abc import abstractmethod, ABC


class AbstractCountryRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
