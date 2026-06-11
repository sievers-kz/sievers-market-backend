from uuid import UUID

from sqlalchemy import ForeignKey, Index, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.catalog.domain.enums import CatalogStatus
from src.core.shared.infrastructure.base_model import BaseModel


class Rubric(BaseModel):
    __tablename__ = "rubrics"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    attributes: Mapped[list] = mapped_column(JSONB, nullable=True, default=list)
    status: Mapped[CatalogStatus] = mapped_column(nullable=False)

    categories: Mapped[list["Category"]] = relationship(
        lazy="selectin",
        cascade="all, delete-orphan"
    )


class Category(BaseModel):
    __tablename__ = "categories"
    rubric_id: Mapped[UUID] = mapped_column(ForeignKey("rubrics.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[CatalogStatus] = mapped_column(nullable=False)

    subcategories: Mapped[list["Subcategory"]] = relationship(
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class Subcategory(BaseModel):
    __tablename__ = "subcategories"
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    attributes: Mapped[list] = mapped_column(JSONB, nullable=True, default=list)
    status: Mapped[CatalogStatus] = mapped_column(nullable=False)

    __table_args__ = (
        Index("ix_subcategory_attributes_gin", "attributes", postgresql_using="gin"),
    )
