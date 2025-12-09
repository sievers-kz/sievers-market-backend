from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Enum, Text, Boolean, DateTime, Index, UniqueConstraint

from src.core.references.domain.enums import MachinerySpecsValueTypeEnum
from src.core.shared.infrastructure.base_model import BaseModel

from src.core.listings.infrastructure.models.listing import Listing, ListingMedia
from src.core.listings.infrastructure.models.machinery import (
    Machinery,
)


class Roubric(BaseModel):
    __tablename__ = "roubrics"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    categories: Mapped[list["MachineryCategory"]] = relationship(
        back_populates="roubric"
    )

    listings: Mapped[list["Listing"]] = relationship(
        back_populates="roubric",
    )


class MachineryManufacturer(BaseModel):
    __tablename__ = "machinery_manufacturers"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    machinery: Mapped[list["Machinery"]] = relationship(
        back_populates="manufacturer"
    )


class MachineryCategory(BaseModel):
    __tablename__ = "machinery_categories"

    roubric_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roubrics.id",
            ondelete="CASCADE"
        )
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    roubric: Mapped["Roubric"] = relationship(
        back_populates="categories"
    )

    subcategories: Mapped[list["MachinerySubcategory"]] = relationship(
        back_populates="category",
        lazy="selectin"
    )


class MachinerySubcategory(BaseModel):
    __tablename__ = "machinery_subcategories"

    category_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_categories.id",
            ondelete="CASCADE"
        )
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    category: Mapped["MachineryCategory"] = relationship(
        back_populates="subcategories"
    )

    machinery: Mapped["Machinery"] = relationship(
        back_populates="subcategory"  # <--- ВОТ ОТКУДА ИДЕТ ССЫЛКА!
    )

    specifications: Mapped[list["MachinerySubcategorySpecification"]] = relationship(
        back_populates="subcategory",
        cascade="all, delete-orphan"
    )


class MachineryManufacturerCountry(BaseModel):
    __tablename__ = "machinery_manufacturer_countries"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    machinery: Mapped[list["Machinery"]] = relationship(
        back_populates="manufacturer_country"
    )


class UnitOfMeasure(BaseModel):
    __tablename__ = "unit_of_measure"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    label: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    specifications: Mapped[list["MachinerySubcategorySpecification"]] = relationship(
        back_populates="unit"
    )


class MachinerySpecificationGroup(BaseModel):
    __tablename__ = "machinery_specification_groups"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True  # engine, transmission, dimensions
    )

    label: Mapped[str] = mapped_column(
        String(100),
        nullable=False  # "Двигатель", "Трансмиссия"
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0  # Порядок отображения на фронте
    )

    specifications: Mapped[list["MachinerySpecification"]] = relationship(
        back_populates="group"
    )


class Region(BaseModel):
    __tablename__ = "regions"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    listings: Mapped[list["Listing"]] = relationship(
        back_populates="region",
    )


class Color(BaseModel):
    __tablename__ = "colors"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    hex: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    machinery: Mapped[list["Machinery"]] = relationship(
        back_populates="color"
    )


class MachinerySpecification(BaseModel):
    __tablename__ = "machinery_specifications"

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

    group: Mapped["MachinerySpecificationGroup | None"] = relationship(
        back_populates="specifications"
    )

    subcategories: Mapped[list["MachinerySubcategorySpecification"]] = relationship(
        back_populates="specification",
        cascade="all, delete-orphan"
    )


class MachinerySubcategorySpecification(BaseModel):
    __tablename__ = "machinery_subcategory_specification"

    subcategory_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_subcategories.id",
            ondelete="CASCADE"
        )
    )

    specification_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery_specifications.id",
            ondelete="CASCADE"
        )
    )

    unit_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "unit_of_measure.id",
            ondelete="CASCADE"
        ),
        nullable=True
    )

    is_required: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        default=False
    )

    subcategory: Mapped["MachinerySubcategory"] = relationship(
        back_populates="specifications"
    )

    specification: Mapped["MachinerySpecification"] = relationship(
        back_populates="subcategories"
    )

    unit: Mapped["UnitOfMeasure | None"] = relationship(
        back_populates="specifications"
    )

    __table_args__ = (
        UniqueConstraint(
            "subcategory_id",
            "specification_id",
            "unit_id",
            name="uq_subcategory_spec_unit"
        ),
    )
