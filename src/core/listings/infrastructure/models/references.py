from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Enum, Text, Boolean, DateTime, Index, UniqueConstraint

from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.listings.infrastructure.models.listing import Listing
    from src.core.listings.infrastructure.models.machinery import MachinerySpecification, Machinery


class Roubric(BaseModel):
    __tablename__ = "roubrics"

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
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
        back_populates="subcategories",
    )

    specifications: Mapped[list["MachinerySpecification"]] = relationship(
        back_populates="subcategory",
        lazy="selectin"
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

    specifications: Mapped[list["MachinerySpecification"]] = relationship(
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
