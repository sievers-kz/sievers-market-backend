from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.iam.domain.enums import TokenType
from src.core.shared.infrastructure.base_model import BaseModel


class Account(BaseModel):
    __tablename__ = "accounts"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default="false"
    )

    tokens: Mapped[list["Token"]] = relationship(
        back_populates="account", cascade="all, delete-orphan", lazy="selectin"
    )


class Token(BaseModel):
    __tablename__ = "tokens"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False
    )

    type: Mapped[TokenType] = mapped_column(nullable=False)

    value: Mapped[str] = mapped_column(Text, nullable=False)

    is_revoked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default="false"
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    account: Mapped["Account"] = relationship(back_populates="tokens")
