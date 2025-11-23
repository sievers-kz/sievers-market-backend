import uuid
from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, Text, DateTime, func, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.shared.infrastructure.base_model import BaseModel
from src.core.auth.domain.enums import TokenTypeEnum


class UserIdentity(BaseModel):
    __tablename__ = "user_identity"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )

    credentials: Mapped["UserCredentialsIdentity"] = relationship(
        back_populates="user_identity",
        cascade="all, delete-orphan",
        uselist=False,
    )

    tokens: Mapped[List["UserTokenIdentity"]] = relationship(
        back_populates="user_identity",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class UserCredentialsIdentity(BaseModel):
    __tablename__ = "user_credentials_identity"

    auth_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_identity.id", ondelete="CASCADE"),
        unique=True
    )

    hashed_password: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    password_changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user_identity: Mapped["UserIdentity"] = relationship(back_populates="credentials")


class UserTokenIdentity(BaseModel):
    __tablename__ = "user_tokens_identity"

    auth_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_identity.id", ondelete="CASCADE")
    )

    token_type: Mapped[TokenTypeEnum] = mapped_column(
        Enum(TokenTypeEnum),
        nullable=False
    )

    token_value: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    user_identity: Mapped["UserIdentity"] = relationship(back_populates="tokens")