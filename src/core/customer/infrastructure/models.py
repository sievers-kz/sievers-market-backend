from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.customer.domain.enums import Kind
from src.core.shared.infrastructure.base_model import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"

    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, unique=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    patronymic: Mapped[str | None] = mapped_column(String(50), nullable=True)


class Organization(BaseModel):
    __tablename__ = "organizations"

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False)
    legal_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    legal_address: Mapped[str | None] = mapped_column(String, nullable=True)
    tax_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    kind: Mapped[Kind] = mapped_column(nullable=False)
    form: Mapped[str | None] = mapped_column(nullable=True)
    shop_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    logo_media_id: Mapped[UUID | None] = mapped_column(ForeignKey("media.id", ondelete="SET NULL"), nullable=True)
    is_registry_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_ownership_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
