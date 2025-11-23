from sqlalchemy.dialects.postgresql import JSONB

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Integer, Enum, Text, Boolean, DateTime, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.listings.domain.enums import (
    MachineryConditionEnum,
    MachinerySpecsValueTypeEnum,
)

from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.listings.infrastructure.models.listing import Listing
    from src.core.shared.infrastructure.shared_models import Color
    from src.core.listings.infrastructure.models.references import (
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
        )
    )

    manufacturer_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_manufacturers.id",
            ondelete="CASCADE"
        )
    )

    manufacturer_country_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_manufacturer_countries.id",
            ondelete="CASCADE"
        )
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
        nullable=False
    )

    year_of_issue: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    condition: Mapped[MachineryConditionEnum] = mapped_column(
        Enum(MachineryConditionEnum),
        nullable=False
    )

    extra_specs: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default={}
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


class MachinerySpecification(BaseModel):
    __tablename__ = "machinery_specifications"

    subcategory_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_subcategories.id",
            ondelete="CASCADE"
        )
    )

    key: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    label: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    value_type: Mapped[MachinerySpecsValueTypeEnum] = mapped_column(
        Enum(MachinerySpecsValueTypeEnum),
        nullable=False
    )

    unit_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "unit_of_measure.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        default=False
    )

    group_id: Mapped[UUID | None] = mapped_column(  # ← ИЗМЕНЕНО!
        ForeignKey(
            "machinery_specification_groups.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    options: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=None
    )

    subcategory: Mapped["MachinerySubcategory"] = relationship(
        back_populates="specifications"
    )

    unit: Mapped["UnitOfMeasure | None"] = relationship(
        back_populates="specifications"
    )

    group: Mapped["MachinerySpecificationGroup | None"] = relationship(
        back_populates="specifications"
    )

    __table_args__ = (
        UniqueConstraint(
            "subcategory_id", "key", name="uq_subcategory_key"
        ),
        Index(
            "ix_machinery_spec_subcategory", "subcategory_id"
        ),
        Index(
            "ix_machinery_spec_group", "group_id"
        )
    )