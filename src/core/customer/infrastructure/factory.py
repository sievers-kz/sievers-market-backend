import uuid
from uuid import UUID

from src.core.customer.domain.entities import Customer
from src.core.customer.domain.value_objects import Fullname


class CustomerFactory:
    @staticmethod
    def create(account_id: UUID, last_name: str, first_name: str) -> Customer:
        return Customer(
            id=uuid.uuid4(),
            account_id=account_id,
            fullname=Fullname(
                last_name=last_name,
                first_name=first_name,
            ),
        )

