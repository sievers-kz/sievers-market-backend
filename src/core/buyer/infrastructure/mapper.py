from src.core.buyer.domain.entities import Buyer as DomainBuyer
from src.core.buyer.infrastructure.models import Buyer as ORMBuyer
from src.core.buyer.domain.value_objects import Fullname


class BuyerMapper:
    @staticmethod
    def to_orm(buyer: DomainBuyer) -> ORMBuyer:
        return ORMBuyer(
            id=buyer.id,
            account_id=buyer.account_id,
            last_name=buyer.fullname.last_name,
            first_name=buyer.fullname.first_name,
            patronymic=buyer.fullname.patronymic,
            city_id=buyer.city_id,
            avatar_url=buyer.avatar_url
        )

    @staticmethod
    def to_domain(buyer: ORMBuyer) -> DomainBuyer:
        return DomainBuyer(
            id=buyer.id,
            account_id=buyer.account_id,
            fullname=Fullname(
                last_name=buyer.last_name,
                first_name=buyer.first_name,
                patronymic=buyer.patronymic
            ),
            city_id=buyer.city_id,
            avatar_url=buyer.avatar_url
        )
