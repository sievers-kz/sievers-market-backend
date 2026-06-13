import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import UUID

from src.core.shared.domain.entities import AggregateRoot
from src.core.vendor.domain.enums import LegalForm, VendorStatus
from src.core.vendor.domain.exceptions import (
    VendorAlreadyVerifiedError,
    VendorCannotBeRestoredError,
)
from src.core.vendor.domain.value_objects import ContactFullname, Logotype, TaxID


@dataclass(frozen=False)
class Vendor(AggregateRoot):
    id: UUID
    account_id: UUID
    contact_fullname: ContactFullname

    legal_name: str
    legal_address: str
    tax_id: TaxID
    legal_form: LegalForm

    contact_phone: str | None = None
    shop_name: str | None = None
    logotype: Logotype | None = None

    is_verified: bool = False
    status: VendorStatus = VendorStatus.ACTIVE
    closed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        account_id: UUID,
        contact_last_name: str,
        contact_first_name: str,
        legal_name: str,
        legal_address: str,
        tax_id: str,
        legal_form: LegalForm,
    ):
        return cls(
            id=uuid.uuid4(),
            account_id=account_id,
            contact_fullname=ContactFullname(contact_last_name, contact_first_name),
            legal_name=legal_name,
            legal_address=legal_address,
            tax_id=TaxID(tax_id, legal_form),
            legal_form=legal_form,
            is_verified=False,
            status=VendorStatus.ACTIVE,
        )

    def verify(self):
        if self.is_verified:
            raise VendorAlreadyVerifiedError()
        self.is_verified = True

    def close(self):
        self.status = VendorStatus.CLOSED
        self.closed_at = datetime.now(timezone.utc)

    def is_restorable(self) -> bool:
        if self.status != VendorStatus.CLOSED:
            return False
        if not self.closed_at:
            return False
        return datetime.now(timezone.utc) - self.closed_at <= timedelta(days=30)

    def restore(self):
        if not self.is_restorable():
            raise VendorCannotBeRestoredError()
        self.status = VendorStatus.ACTIVE
        self.closed_at = None

    def ban(self):
        self.status = VendorStatus.BANNED

    def change_contact_fullname(
        self, contact_last_name: str, contact_first_name: str, contact_patronymic: str
    ):
        self.contact_fullname = ContactFullname(
            contact_last_name=contact_last_name,
            contact_first_name=contact_first_name,
            contact_patronymic=contact_patronymic,
        )

    def change_contact_phone(self, raw_contact_phone: str):
        self.contact_phone = raw_contact_phone

    def change_shop_name(self, raw_shop_name: str):
        self.shop_name = raw_shop_name

    def change_logotype(self, raw_logotype: dict):
        self.logotype = Logotype.from_dict(raw_logotype)
