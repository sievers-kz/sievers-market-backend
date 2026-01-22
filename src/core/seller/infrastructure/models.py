from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.seller.domain.enums import SellerType
from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.iam.infrastructure.models import Account
    from src.core.references.infrastructure.models import City


class Seller(BaseModel):
    __tablename__ = "sellers"

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

    seller_type: Mapped[SellerType] = mapped_column(
        Enum(
            SellerType,
            native_enum=False,
            values_callable=BaseModel.get_enum_values
        ),
        nullable=False
    )

    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    legal_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    tax_id: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
        unique=True,
        index=True
    )

    city_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "cities.id",
            ondelete="SET NULL"
        ),
        nullable=False
    )

    logotype_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        server_default="default_logotype.png"
    )

    account: Mapped["Account"] = relationship()
    city: Mapped["City"] = relationship()