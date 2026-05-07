from dataclasses import dataclass
from uuid import UUID

from src.core.customer.domain.value_objects import Fullname
from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Customer(AggregateRoot):
    id: UUID
    account_id: UUID
    fullname: Fullname
    avatar_url: str | None = None

    def change_fullname(self, last_name: str, first_name: str, patronymic: str | None):
        self.fullname = Fullname(last_name=last_name, first_name=first_name, patronymic=patronymic)

