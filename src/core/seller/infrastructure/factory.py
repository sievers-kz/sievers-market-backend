import uuid
from uuid import UUID
from src.core.seller.domain.entities import Seller
from src.api.iam.dto import CreateSellerRequest
from src.core.seller.domain.value_objects import Fullname, CompanyName, TaxID


class SellerFactory:
    @staticmethod
    def create(account_id: UUID, dto: CreateSellerRequest) -> Seller:
        return Seller(
            id=uuid.uuid4(),
            account_id=account_id,
            fullname=Fullname(
                last_name=dto.last_name,
                first_name=dto.first_name,
            ),
            seller_type=dto.seller_type,
            company_name=CompanyName(dto.company_name),
            legal_address=dto.legal_address,
            tax_id=TaxID(dto.tax_id),
            city_id=dto.city_id
        )
