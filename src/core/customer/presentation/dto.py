from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.shared.presentation.dto import DTO


class ChangeCustomerFullname(BaseModel):
    last_name: str
    first_name: str
    patronymic: str | None = None


class CreateOrganizationRequest(DTO):
    kind: Kind
    tax_id: str = Field(pattern=r"^\d{12}$")


class CreateOrganizationResponse(DTO):
    id: UUID
    registry_status: RegistryStatus


class TaxpayerResponse(DTO):
    tax_id: str
    legal_name: str
    kind: Kind
    is_active: bool = True


class CustomerMeResponse(DTO):
    id: UUID
    email: str
    password_changed_at: datetime
    last_name: str | None = None
    first_name: str | None = None
    patronymic: str | None = None


class OrganizationListResponse(DTO):
    id: UUID
    tax_id: str
    kind: Kind
    registry_status: RegistryStatus
    is_ownership_verified: bool
    legal_name: str | None = None
    shop_name: str | None = None
    logo_media_id: UUID | None = None


class OrganizationResponse(DTO):
    id: UUID
    tax_id: str
    kind: Kind
    registry_status: RegistryStatus
    is_ownership_verified: bool
    legal_name: str | None = None
    legal_address: str | None = None
    form: str | None = None
    shop_name: str | None = None
    logo_media_id: UUID | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
