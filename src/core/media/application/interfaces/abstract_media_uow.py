from abc import ABC, abstractmethod

from src.core.media.application.interfaces.abstract_media_repository import AbstractMediaRepository


class AbstractMediaUnitOfWork(ABC):
    @property
    @abstractmethod
    def media(self) -> AbstractMediaRepository:
        raise NotImplementedError
