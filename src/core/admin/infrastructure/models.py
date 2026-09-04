from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.admin.domain.enums import AdminRoles
from src.core.shared.infrastructure.base_model import BaseModel


class Admin(BaseModel):
    __tablename__ = "admins"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"), unique=True
    )

    last_name: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[AdminRoles] = mapped_column(nullable=False)

    permissions: Mapped[list["Permission"]] = relationship(
        secondary="admin_permissions",
        lazy="selectin",
    )


class Permission(BaseModel):
    __tablename__ = "permissions"

    codename: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)


class AdminPermission(BaseModel):
    __tablename__ = "admin_permissions"

    admin_id: Mapped[UUID] = mapped_column(
        ForeignKey("admins.id", ondelete="CASCADE"), primary_key=True
    )
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
    )
