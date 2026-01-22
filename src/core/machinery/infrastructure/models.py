from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Integer, Enum, BigInteger, Text, Index, Computed
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.machinery.domain.enums import MachineryCondition, PriceCurrency, ListingStatus
from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.seller.infrastructure.models import Seller
    from src.core.references.infrastructure.models import Subcategory, City, Brand, Color, Country


class Machinery(BaseModel):
    __tablename__ = "machinery"

    seller_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "sellers.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    subcategory_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "subcategories.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    title: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    price: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    currency: Mapped[PriceCurrency | None] = mapped_column(
        Enum(
            PriceCurrency,
            native_enum=False,
            values_callable=BaseModel.get_enum_values
        ),
        nullable=True
    )

    city_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "cities.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    brand_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "brands.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    model: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    year_of_issue: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    condition: Mapped[MachineryCondition | None] = mapped_column(
        Enum(
            MachineryCondition,
            native_enum=False,
            values_callable=BaseModel.get_enum_values
        ),
        nullable=True
    )

    color_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "colors.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    attributes: Mapped[dict | None] = mapped_column(
        JSONB,
        default={},
        nullable=True
    )

    country_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "countries.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    status: Mapped[ListingStatus] = mapped_column(
        Enum(
            ListingStatus,
            native_enum=False,
            values_callable=BaseModel.get_enum_values
        ),
        default=ListingStatus.DRAFT,
        nullable=False
    )

    engine_power: Mapped[int | None] = mapped_column(
        Integer,
        Computed("(attributes->>'engine_power')::integer", persisted=True),
        nullable=True
    )

    weight: Mapped[int | None] = mapped_column(
        Integer,
        Computed("(attributes->>'weight')::integer", persisted=True),
        nullable=True
    )

    __table_args__ = (
        Index("ix_machinery_attributes_gin", "attributes", postgresql_using="gin"),
        Index("ix_machinery_engine_power", "engine_power"),
        Index("ix_machinery_weight", "weight")
    )

    seller: Mapped["Seller"] = relationship()
    subcategory: Mapped["Subcategory"] = relationship()
    city: Mapped["City | None"] = relationship()
    brand: Mapped["Brand | None"] = relationship()
    color: Mapped["Color | None"] = relationship()
    country: Mapped["Country | None"] = relationship()
