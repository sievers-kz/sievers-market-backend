from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, BigInteger, Enum, Text, Integer, Computed, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.machinery.domain.enums import MachineryCondition
from src.core.shared.domain.enums import PriceCurrency, ListingStatus
from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.customer.infrastructure.models import Customer
    from src.core.catalog.infrastructure.models import Subcategory
    from src.core.references.infrastructure.models import City
    from src.core.references.infrastructure.models import Brand
    from src.core.references.infrastructure.models import Color
    from src.core.references.infrastructure.models import Country


class Machinery(BaseModel):
    __tablename__ = "machinery"

    customer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "customers.id",
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
        String,
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
        String,
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

    country_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "countries.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    attributes: Mapped[dict | None] = mapped_column(
        JSONB,
        default={},
        nullable=True
    )

    status: Mapped[ListingStatus] = mapped_column(
        Enum(
            ListingStatus,
            native_enum=False,
            values_callable=BaseModel.get_enum_values
        ),
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

    length: Mapped[int | None] = mapped_column(
        Integer,
        Computed("(attributes->>'length')::integer", persisted=True),
        nullable=True
    )

    width: Mapped[int | None] = mapped_column(
        Integer,
        Computed("(attributes->>'width')::integer", persisted=True),
        nullable=True
    )

    height: Mapped[int | None] = mapped_column(
        Integer,
        Computed("(attributes->>'height')::integer", persisted=True),
        nullable=True
    )

    __table_args__ = (
        Index("ix_machinery_attributes_gin", "attributes", postgresql_using="gin"),
        Index("ix_machinery_engine_power", "engine_power"),
        Index("ix_machinery_weight", "weight"),
        Index("ix_machinery_length", "length"),
        Index("ix_machinery_width", "width"),
        Index("ix_machinery_height", "height"),
    )

    customer: Mapped["Customer"] = relationship()
    subcategory: Mapped["Subcategory"] = relationship()
    city: Mapped["City | None"] = relationship()
    brand: Mapped["Brand | None"] = relationship()
    color: Mapped["Color | None"] = relationship()
    country: Mapped["Country | None"] = relationship()
