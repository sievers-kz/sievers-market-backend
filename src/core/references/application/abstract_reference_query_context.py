from abc import ABC, abstractmethod


class AbstractReferenceQueryContext(ABC):
    @property
    @abstractmethod
    def reference(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def category(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def specification(self):
        raise NotImplementedError
