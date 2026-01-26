from abc import ABC, abstractmethod


class AbstractObjectStorage(ABC):
    @abstractmethod
    def generate_presigned_url(self, object_name: str, expiration: int = 3600):
        raise NotImplementedError
