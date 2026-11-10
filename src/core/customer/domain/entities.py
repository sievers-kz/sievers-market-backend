import uuid
from dataclasses import dataclass
from uuid import UUID

from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.customer.domain.value_objects import Fullname
from src.core.shared.domain.entities import AggregateRoot


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

    def mark_registry_verified(self, legal_name: str) -> None:
        self.legal_name = legal_name
        self.registry_status = RegistryStatus.VERIFIED

    def mark_registry_not_found(self) -> None:
        self.registry_status = RegistryStatus.NOT_FOUND

    def can_publish(self) -> bool:
        return self.registry_status == RegistryStatus.VERIFIED
