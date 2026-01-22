from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Enum, Boolean, Index

from src.core.references.domain.enums import AttrValueType
from src.core.shared.infrastructure.base_model import BaseModel


class Rubric(BaseModel):
    __tablename__ = "rubrics"
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    categories: Mapped[list["Category"]] = relationship(
        back_populates="rubric",
        lazy="selectin",
        cascade="all, delete-orphan"
    )


class Category(BaseModel):
    __tablename__ = "categories"
    rubric_id: Mapped[UUID] = mapped_column(ForeignKey("rubrics.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    rubric: Mapped["Rubric"] = relationship(back_populates="categories")

    subcategories: Mapped[list["Subcategory"]] = relationship(
        back_populates="category",
        lazy="selectin",
        cascade="all, delete-orphan",
        order_by="Subcategory.position"
    )


class Subcategory(BaseModel):
    __tablename__ = "subcategories"
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    category: Mapped["Category"] = relationship(back_populates="subcategories")

    subcategory_attributes: Mapped[list["SubcategoryAttribute"]] = relationship(
        back_populates="subcategory",
        cascade="all, delete-orphan"
    )


class AttrGroup(BaseModel):
    __tablename__ = "attr_groups"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0)

    attributes: Mapped[list["Attribute"]] = relationship(back_populates="group")


class Attribute(BaseModel):
    __tablename__ = "attributes"
    group_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(
            "attr_groups.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    key: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)

    value_type: Mapped[AttrValueType] = mapped_column(
        Enum(
            AttrValueType,
            native_enum=False,
            values_callable=BaseModel.get_enum_values
        ),
        nullable=False
    )

    position: Mapped[int] = mapped_column(Integer, default=0)

    group: Mapped[Optional["AttrGroup"]] = relationship(back_populates="attributes")
    subcategory_attributes: Mapped[list["SubcategoryAttribute"]] = relationship(back_populates="attribute")

    options: Mapped[Optional[list["AttributeOption"]]] = relationship(
        back_populates="attribute",
        cascade="all, delete-orphan"
    )


class AttributeOption(BaseModel):
    __tablename__ = "attribute_options"

    attribute_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "attributes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    key: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)

    attribute: Mapped["Attribute"] = relationship(back_populates="options")


class SubcategoryAttribute(BaseModel):
    """Таблица-мостик между подкатегориями и атрибутами"""
    __tablename__ = "subcategory_attributes"

    subcategory_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "subcategories.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    attribute_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "attributes.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    unit_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(
            "unit_of_measure.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    is_required: Mapped[bool] = mapped_column(Boolean, default=False)
    is_filterable: Mapped[bool] = mapped_column(Boolean, default=False)

    subcategory: Mapped["Subcategory"] = relationship(back_populates="subcategory_attributes")
    attribute: Mapped["Attribute"] = relationship(back_populates="subcategory_attributes")
    unit: Mapped[Optional["UnitOfMeasure"]] = relationship()

    __table_args__ = (
        Index(
            "uq_sub_attr_unit",
            "subcategory_id",
            "attribute_id",
            "unit_id",
            unique=True,
            postgresql_nulls_not_distinct=True
        ),
    )


class UnitOfMeasure(BaseModel):
    __tablename__ = "unit_of_measure"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    label: Mapped[str] = mapped_column(String(50), nullable=False)


class Brand(BaseModel):
    __tablename__ = "brands"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Country(BaseModel):
    __tablename__ = "countries"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Region(BaseModel):
    __tablename__ = "regions"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cities: Mapped[list["City"]] = relationship(back_populates="region", cascade="all, delete-orphan")


class City(BaseModel):
    __tablename__ = "cities"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    region_id: Mapped[UUID] = mapped_column(ForeignKey("regions.id", ondelete="CASCADE"), nullable=False)
    region: Mapped["Region"] = relationship(back_populates="cities")


class Color(BaseModel):
    __tablename__ = "colors"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hex: Mapped[str] = mapped_column(String(50), nullable=False)