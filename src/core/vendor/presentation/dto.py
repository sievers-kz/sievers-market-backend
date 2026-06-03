from uuid import UUID

from src.core.shared.presentation.dto import DTO
from src.core.vendor.domain.enums import LegalForm


class CreateVendorRequest(DTO):
    contact_last_name: str
    contact_first_name: str
    legal_name: str
    legal_address: str
    tax_id: str
    legal_form: LegalForm


class VendorValidationResponse(DTO):
    tax_id: str
    name: str
    type: LegalForm
    is_liquidation: bool


class ChangeContactFullnameRequest(DTO):
    contact_last_name: str
    contact_first_name: str
    contact_patronymic: str


class ChangeShopNameRequest(DTO):
    shop_name: str


class ChangeLogotypeRequest(DTO):
    logotype: dict


class ChangeContactPhoneRequest(DTO):
    contact_phone: str


class VendorProfileResponse(DTO):
    account_id: UUID
    vendor_id: UUID
    email: str
    is_verified: bool
    contact_last_name: str
    contact_first_name: str
    contact_patronymic: str | None
    contact_phone: str | None
    legal_name: str
    legal_address: str
    tax_id: str
    legal_form: LegalForm
    shop_name: str | None
    logotype: dict | None

