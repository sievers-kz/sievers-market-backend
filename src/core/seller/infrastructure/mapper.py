from src.core.seller.domain.entities import Seller as DomainSeller
from src.core.seller.domain.value_objects import Fullname, CompanyName, TaxID
from src.core.seller.infrastructure.models import Seller as ORMSeller


class SellerMapper:
    @staticmethod
    def to_orm(seller: DomainSeller) -> ORMSeller:
        return ORMSeller(
            id=seller.id,
            account_id=seller.account_id,
            last_name=seller.fullname.last_name,
            first_name=seller.fullname.first_name,
            patronymic=seller.fullname.patronymic,
            seller_type=seller.seller_type,
            company_name=seller.company_name.value,
            legal_address=seller.legal_address,
            tax_id=seller.tax_id.value,
            city_id=seller.city_id,
            logotype_url=seller.logotype_url if seller.logotype_url else None
        )

    @staticmethod
    def to_domain(seller: ORMSeller) -> DomainSeller:
        return DomainSeller(
            id=seller.id,
            account_id=seller.account_id,
            fullname=Fullname(
                last_name=seller.last_name,
                first_name=seller.first_name,
                patronymic=seller.patronymic
            ),
            seller_type=seller.seller_type,
            company_name=CompanyName(seller.company_name),
            legal_address=seller.legal_address,
            tax_id=TaxID(seller.tax_id),
            city_id=seller.city_id,
            logotype_url=seller.logotype_url
        )
