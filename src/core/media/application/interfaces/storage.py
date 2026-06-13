from abc import ABC, abstractmethod


class IObjectStorage(ABC):
    @abstractmethod
    def generate_upload_url(self, object_name: str, expiration: int = 3600) -> str:
        raise NotImplementedError
