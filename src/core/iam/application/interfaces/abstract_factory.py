from abc import ABC, abstractmethod
from uuid import UUID

from src.core.iam.domain.entities import Account


class AbstractAccountFactory(ABC):
    @abstractmethod
    def create(self, account_id: UUID, account_data, token_data) -> Account:
        raise NotImplementedError

