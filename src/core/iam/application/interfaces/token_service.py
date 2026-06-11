from abc import ABC, abstractmethod
from uuid import UUID


class ITokenService(ABC):
    @abstractmethod
    def create_token(self, user_id: UUID, token_type):
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str, expected_type) -> dict:
        raise NotImplementedError
