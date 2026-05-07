from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.iam.infrastructure.models import Account


class Customer(BaseModel):
    __tablename__ = "customers"

    account_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "accounts.id",
            ondelete="CASCADE"
        ),
        nullable=False,
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

    patronymic: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        server_default="default_avatar.png"
    )

    account: Mapped["Account"] = relationship()
