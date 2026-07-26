from datetime import datetime
from uuid import UUID

from pydantic import Field

from src.core.shared.presentation.dto import DTO
from src.core.vendor.domain.enums import LegalForm


class CreateVendorRequest(DTO):
    contact_last_name: str
    contact_first_name: str
    legal_name: str
    legal_address: str
    tax_id: str
    legal_form: LegalForm


class TaxpayerResponse(DTO):
    tax_id: str
    legal_name: str
    legal_form: LegalForm
    is_liquidation: bool


class ChangeContactFullnameRequest(DTO):
    contact_last_name: str
    contact_first_name: str
    contact_patronymic: str | None = None


class ChangeShopNameRequest(DTO):
    shop_name: str


class ChangeLogotypeRequest(DTO):
    logotype: dict = Field(
        default_factory=dict,
        json_schema_extra={
            "example": {
                "media_id": "uuid-1",
                "media_type": "image/png",
                "media_size": 1,
            }
        },
    )


class ChangeContactPhoneRequest(DTO):
    contact_phone: str


class VendorProfileResponse(DTO):
    account_id: UUID
    vendor_id: UUID
    email: str
    password_changed_at: datetime
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


class VendorListingCardsResponse(DTO):
    listing_id: UUID
    subcategory: str
    title: str
    price: int
    currency: str
    updated_at: datetime
    city: str
    preview_image: UUID
