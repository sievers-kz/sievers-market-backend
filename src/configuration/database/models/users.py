import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, String, DateTime, func, ForeignKey, Enum, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.users.domain.enums import UserRoleEnum, BusinessTypeEnum, TokenTypeEnum
from src.configuration.database.connection import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class User(BaseModel):
    __tablename__ = "users"

    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(25), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)

    individual_profile: Mapped["IndividualProfile"] = relationship(back_populates="user", uselist=False)
    business_profile: Mapped["BusinessProfile"] = relationship(back_populates="user", uselist=False)
    auth: Mapped["UserAuth"] = relationship(back_populates="user", uselist=False)
    tokens: Mapped[list["AuthToken"]] = relationship(back_populates="user")


class IndividualProfile(BaseModel):
    __tablename__ = "individual_profiles"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    user: Mapped["User"] = relationship(back_populates="individual_profile")


class BusinessProfile(BaseModel):
    __tablename__ = "business_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    user: Mapped["User"] = relationship(back_populates="business_profile")
    business_type: Mapped[BusinessTypeEnum] = mapped_column(Enum(BusinessTypeEnum), nullable=False)
    organization_fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    iin: Mapped[str] = mapped_column(String(12), nullable=True, unique=True)
    bin: Mapped[str] = mapped_column(String(12), nullable=True, unique=True)


class UserAuth(BaseModel):
    __tablename__ = "user_auth"
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    user: Mapped["User"] = relationship(back_populates="auth")


class AuthToken(BaseModel):
    __tablename__ = "auth_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_type: Mapped[TokenTypeEnum] = mapped_column(Enum(TokenTypeEnum), nullable=False)
    token_value: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user: Mapped["User"] = relationship(back_populates="tokens")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
