from sqlalchemy.dialects.postgresql import JSONB

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Integer, Enum, Text, Boolean, DateTime, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.listings.domain.enums import (
    MachineryConditionEnum,
)

from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.listings.infrastructure.models.listing import Listing
    from src.core.references.infrastructure.models import Color
    from src.core.references.infrastructure.models import (
        MachinerySubcategory,
        MachineryManufacturer,
        MachineryManufacturerCountry,
        UnitOfMeasure,
        MachinerySpecificationGroup
    )


class Machinery(BaseModel):
    __tablename__ = "machinery"

    listing_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "listings.id",
            ondelete="CASCADE"
        )
    )

    subcategory_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_subcategories.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    manufacturer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_manufacturers.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )

    manufacturer_country_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_manufacturer_countries.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )

    color_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "colors.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    year_of_issue: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    condition: Mapped[MachineryConditionEnum] = mapped_column(
        Enum(MachineryConditionEnum),
        nullable=True
    )

    extra_specs: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
        default=dict
    )

    listing: Mapped["Listing"] = relationship(
        back_populates="machinery"
    )

    subcategory: Mapped["MachinerySubcategory"] = relationship(
        back_populates="machinery"
    )

    manufacturer: Mapped["MachineryManufacturer"] = relationship(
        back_populates="machinery"
    )

    manufacturer_country: Mapped["MachineryManufacturerCountry"] = relationship(
        back_populates="machinery"
    )

    color: Mapped["Color | None"] = relationship(
        back_populates="machinery"
    )

    __table_args__ = (
        Index(
            "ix_machinery_extra_specs_gin", "extra_specs", postgresql_using="gin"
        ),
    )


