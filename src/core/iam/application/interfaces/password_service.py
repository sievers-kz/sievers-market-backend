from abc import ABC, abstractmethod


class IPasswordService(ABC):
    @abstractmethod
    def validate(self, raw: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def hash(self, raw: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify(self, raw: str, hash: str) -> bool:
        raise NotImplementedError
