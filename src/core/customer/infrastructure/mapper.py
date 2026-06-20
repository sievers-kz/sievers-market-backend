from src.core.customer.domain.entities import Customer as DomainCustomer
from src.core.customer.domain.value_objects import Fullname
from src.core.customer.infrastructure.models import Customer as ORMCustomer


class CustomerMapper:
    @staticmethod
    def to_orm(buyer: DomainCustomer) -> ORMCustomer:
        return ORMCustomer(
            id=buyer.id,
            account_id=buyer.account_id,
            last_name=buyer.fullname.last_name,
            first_name=buyer.fullname.first_name,
            patronymic=buyer.fullname.patronymic,
            avatar_url=buyer.avatar_url,
        )

    @staticmethod
    def to_domain(buyer: ORMCustomer) -> DomainCustomer:
        return DomainCustomer(
            id=buyer.id,
            account_id=buyer.account_id,
            fullname=Fullname(
                last_name=buyer.last_name,
                first_name=buyer.first_name,
                patronymic=buyer.patronymic,
            ),
            avatar_url=buyer.avatar_url,
        )
