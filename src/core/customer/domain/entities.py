import uuid
from dataclasses import dataclass
from uuid import UUID

from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.customer.domain.exceptions import (
    InvalidShopNameError,
    OrganizationCannotPublishError,
    OrganizationNotFoundError,
)
from src.core.customer.domain.value_objects import Fullname
from src.core.shared.domain.entities import AggregateRoot

SHOP_NAME_MIN_LENGTH = 2
SHOP_NAME_MAX_LENGTH = 50


@dataclass(frozen=False)
class Customer(AggregateRoot):
    id: UUID
    account_id: UUID
    fullname: Fullname | None

    @classmethod
    def create(cls, account_id: UUID):
        return cls(id=uuid.uuid4(), account_id=account_id, fullname=None)

    def change_fullname(self, fullname: Fullname):
        self.fullname = fullname


@dataclass(frozen=False)
class Organization(AggregateRoot):
    id: UUID
    owner_id: UUID
    legal_name: str | None
    legal_address: str | None
    tax_id: str
    kind: Kind
    form: str | None
    shop_name: str | None
    logo_media_id: UUID | None
    contact_phone: str | None
    contact_email: str | None
    is_ownership_verified: bool
    registry_status: RegistryStatus

    @classmethod
    def create(
        cls,
        owner_id: UUID,
        tax_id: str,
        kind: Kind,
    ):
        return cls(
            id=uuid.uuid4(),
            owner_id=owner_id,
            legal_name=None,
            legal_address=None,
            tax_id=tax_id,
            kind=kind,
            form=None,
            shop_name=None,
            logo_media_id=None,
            contact_phone=None,
            contact_email=None,
            is_ownership_verified=False,
            registry_status=RegistryStatus.PENDING,
        )

    def mark_registry_verified(self, legal_name: str, legal_address: str | None = None) -> None:
        self.legal_name = legal_name
        self.legal_address = legal_address
        self.registry_status = RegistryStatus.VERIFIED

    def mark_registry_not_found(self) -> None:
        self.registry_status = RegistryStatus.NOT_FOUND

    def change_shop_name(self, shop_name: str) -> None:
        normalized = " ".join(shop_name.split())
        if not SHOP_NAME_MIN_LENGTH <= len(normalized) <= SHOP_NAME_MAX_LENGTH:
            raise InvalidShopNameError()
        if not any(char.isalpha() for char in normalized):
            raise InvalidShopNameError()
        self.shop_name = normalized

    def change_contact_phone(self, contact_phone: str) -> None:
        self.contact_phone = contact_phone

    def change_contact_email(self, contact_email: str) -> None:
        self.contact_email = contact_email

    def is_owned_by(self, owner_id: UUID) -> bool:
        return self.owner_id == owner_id

    def can_publish(self) -> bool:
        return self.registry_status == RegistryStatus.VERIFIED

    def ensure_can_publish(self, owner_id: UUID) -> None:
        # A foreign organization is reported as missing, so its existence is not revealed.
        if not self.is_owned_by(owner_id):
            raise OrganizationNotFoundError()
        if not self.can_publish():
            raise OrganizationCannotPublishError()
