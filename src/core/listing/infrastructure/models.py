from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey as FK
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, BigInteger, Enum, Text

from src.core.shared.domain.enums import PriceCurrency
from src.core.listing.domain.enums import ListingStatus
from src.core.shared.infrastructure.base_model import BaseModel


class Listing(BaseModel):
    __tablename__ = "listings"

    owner_id: Mapped[UUID] = mapped_column(FK("accounts.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(FK("categories.id", ondelete="CASCADE"), nullable=False)
    subcategory_id: Mapped[UUID] = mapped_column(FK("subcategories.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[int] = mapped_column(BigInteger, nullable=True)
    currency: Mapped[PriceCurrency] = mapped_column(nullable=True)

    city_id: Mapped[UUID] = mapped_column(FK("cities.id", ondelete="SET NULL"), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    attributes: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=True, default={})
    gallery: Mapped[list[dict]] = mapped_column(JSONB, nullable=True, default=[])
    status: Mapped[ListingStatus] = mapped_column(nullable=True)
