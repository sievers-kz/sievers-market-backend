from dataclasses import dataclass
from uuid import UUID

from src.core.seller.domain.enums import SellerType
from src.core.seller.domain.value_objects import Fullname, CompanyName, TaxID
from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Seller(AggregateRoot):
    id: UUID
    account_id: UUID
    fullname: Fullname
    seller_type: SellerType
    company_name: CompanyName
    legal_address: str
    tax_id: TaxID
    city_id: UUID
    logotype_url: str | None = None

    def change_fullname(self, last_name: str, first_name: str, patronymic: str | None):
        self.fullname = Fullname(last_name=last_name, first_name=first_name, patronymic=patronymic)

    def change_company_name(self, company_name: str):
        self.company_name = CompanyName(value=company_name)

    def change_tax_id(self, raw_tax_id: str):
        self.tax_id = TaxID(value=raw_tax_id)

