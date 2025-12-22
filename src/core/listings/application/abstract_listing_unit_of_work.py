from abc import abstractmethod, ABC


class AbstractListingUnitOfWork(ABC):
    @property
    @abstractmethod
    def listing(self):
        raise NotImplementedError
