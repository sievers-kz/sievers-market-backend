from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.listings.infrastructure.models.listing import Listing
    from src.core.listings.infrastructure.models.machinery import Machinery, MachinerySpecification


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
