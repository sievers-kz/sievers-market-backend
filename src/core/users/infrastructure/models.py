import uuid

from sqlalchemy import String, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.shared.infrastructure.base_model import BaseModel
from src.core.users.domain.enums import UserRoleEnum, DocumentTypeEnum, BusinessTypeEnum


class User(BaseModel):
    __tablename__ = "users"

    role: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum),
        nullable=False,
        default=UserRoleEnum.INDIVIDUAL.value
    )

    email: Mapped[str] = mapped_column(
        String(256),
        unique=True,
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )

    profile: Mapped["UserProfile"] = relationship(back_populates="user")
    business_details: Mapped["BusinessDetails"] = relationship(back_populates="user")


class UserProfile(BaseModel):
    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    patronymic: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    avatar_url: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="profile")


class BusinessDetails(BaseModel):
    __tablename__ = "business_details"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )

    business_type: Mapped[BusinessTypeEnum] = mapped_column(
        Enum(BusinessTypeEnum),
        nullable=False
    )

    organization_fullname: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    document_type: Mapped[DocumentTypeEnum] = mapped_column(
        Enum(DocumentTypeEnum),
        nullable=False,
    )

    document_value: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
        unique=True
    )

    user: Mapped["User"] = relationship(back_populates="business_details")
