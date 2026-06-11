from datetime import datetime
from uuid import UUID

from sqlalchemy import String, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.core.shared.infrastructure.base_model import BaseModel
from src.core.vendor.domain.enums import LegalForm, VendorStatus


class Vendor(BaseModel):
    __tablename__ = "vendors"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"))

    contact_last_name: Mapped[str] = mapped_column(String, nullable=False)
    contact_first_name: Mapped[str] = mapped_column(String, nullable=False)
    contact_patronymic: Mapped[str] = mapped_column(String, nullable=True)
    contact_phone: Mapped[str] = mapped_column(String, nullable=True)

    legal_name: Mapped[str] = mapped_column(String, nullable=False)
    legal_address: Mapped[str] = mapped_column(String, nullable=False)
    tax_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    legal_form: Mapped[LegalForm] = mapped_column(nullable=False)

    shop_name: Mapped[str] = mapped_column(String, nullable=True)
    logotype: Mapped[dict] = mapped_column(JSONB, nullable=True, default=dict)

    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False)
    status: Mapped[VendorStatus] = mapped_column(nullable=False)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
