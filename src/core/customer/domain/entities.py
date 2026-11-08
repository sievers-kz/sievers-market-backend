import uuid
from dataclasses import dataclass
from uuid import UUID

from src.core.customer.domain.enums import Kind
from src.core.customer.domain.value_objects import Fullname
from src.core.shared.domain.entities import AggregateRoot


@dataclass(frozen=False)
class Customer(AggregateRoot):
    id: UUID
    account_id: UUID
    fullname: Fullname

    @classmethod
    def create(cls, account_id: UUID, fullname: Fullname):
        return cls(id=uuid.uuid4(), account_id=account_id, fullname=fullname)


@dataclass(frozen=False)
class Organization(AggregateRoot):
    id: UUID
    owner_id: UUID
    legal_name: str
    legal_address: str
    tax_id: str
    kind: Kind
    form: str | None
    shop_name: str | None
    logo_media_id: UUID | None
    is_registry_verified: bool
    is_ownership_verified: bool
    contact_phone: str | None
    contact_email: str | None

    @classmethod
    def create(
        cls,
        owner_id: UUID,
        legal_name: str,
        legal_address: str,
        tax_id: str,
        kind: Kind,
    ):
        return cls(
            id=uuid.uuid4(),
            owner_id=owner_id,
            legal_name=legal_name,
            legal_address=legal_address,
            tax_id=tax_id,
            kind=kind,
            form=None,
            shop_name=None,
            logo_media_id=None,
            is_registry_verified=False,
            is_ownership_verified=False,
            contact_phone=None,
            contact_email=None,
        )
