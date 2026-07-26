from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from src.core.catalog.infrastructure.enums import AttributeType, CatalogStatus
from src.core.shared.infrastructure.base_model import BaseModel


class Rubric(BaseModel):
    __tablename__ = "rubrics"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[CatalogStatus] = mapped_column(nullable=False)

    categories: Mapped[list["Category"]] = relationship(
        lazy="selectin", cascade="all, delete-orphan"
    )


class Category(BaseModel):
    __tablename__ = "categories"
    rubric_id: Mapped[UUID] = mapped_column(
        ForeignKey("rubrics.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[CatalogStatus] = mapped_column(nullable=False)

    subcategories: Mapped[list["Subcategory"]] = relationship(
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class Subcategory(BaseModel):
    __tablename__ = "subcategories"
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[CatalogStatus] = mapped_column(nullable=False)


class UnitOfMeasure(BaseModel):
    __tablename__ = "unit_of_measure"
    key: Mapped[str] = mapped_column(String, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)


class AttributeGroup(BaseModel):
    __tablename__ = "attribute_groups"
    key: Mapped[str] = mapped_column(String, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0)


class AttributeDefinition(BaseModel):
    __tablename__ = "attribute_definitions"
    key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[AttributeType] = mapped_column(nullable=False)
    options: Mapped[dict] = mapped_column(JSONB, default=[])


class SubcategoryAttribute(BaseModel):
    __tablename__ = "subcategory_attributes"
    subcategory_id: Mapped[UUID] = mapped_column(
        ForeignKey("subcategories.id", ondelete="CASCADE")
    )
    attribute_id: Mapped[UUID] = mapped_column(
        ForeignKey("attribute_definitions.id", ondelete="CASCADE")
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey("attribute_groups.id", ondelete="RESTRICT")
    )
    unit_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("unit_of_measure.id", ondelete="SET NULL"), nullable=True
    )
    required: Mapped[bool] = mapped_column(Boolean, nullable=False)
    filterable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0)

    attribute: Mapped["AttributeDefinition"] = relationship()
    group: Mapped["AttributeGroup"] = relationship()
    unit: Mapped["UnitOfMeasure | None"] = relationship()
