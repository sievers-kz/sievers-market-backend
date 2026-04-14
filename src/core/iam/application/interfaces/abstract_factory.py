from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from src.core.iam.domain.entities import Account


class IAccountFactory(ABC):
    @abstractmethod
    def create(self, data: Any) -> Account:
        raise NotImplementedError

