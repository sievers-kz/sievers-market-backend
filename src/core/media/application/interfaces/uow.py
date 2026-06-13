from abc import ABC, abstractmethod

from src.core.media.application.interfaces.repository import IMediaRepository


class IMediaUnitOfWork(ABC):
    @property
    @abstractmethod
    def media(self) -> IMediaRepository:
        raise NotImplementedError
