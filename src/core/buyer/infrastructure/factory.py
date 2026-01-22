import uuid
from uuid import UUID

from src.api.iam.dto import CreateBuyerRequest
from src.core.buyer.domain.entities import Buyer
from src.core.buyer.domain.value_objects import Fullname


class BuyerFactory:
    @staticmethod
    def create(account_id: UUID, dto: CreateBuyerRequest) -> Buyer:
        return Buyer(
            id=uuid.uuid4(),
            account_id=account_id,
            fullname=Fullname(
                last_name=dto.last_name,
                first_name=dto.first_name,
            ),
        )

