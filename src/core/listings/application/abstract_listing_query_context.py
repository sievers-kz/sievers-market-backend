from abc import ABC, abstractmethod


class AbstractListingQueryContext(ABC):
    @property
    @abstractmethod
    def listing(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def filter(self):
        raise NotImplementedError
