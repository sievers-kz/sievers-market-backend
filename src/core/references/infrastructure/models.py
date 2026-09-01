from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.shared.infrastructure.base_model import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Country(BaseModel):
    __tablename__ = "countries"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Region(BaseModel):
    __tablename__ = "regions"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cities: Mapped[list["City"]] = relationship(
        back_populates="region", cascade="all, delete-orphan"
    )


class City(BaseModel):
    __tablename__ = "cities"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    region_id: Mapped[UUID] = mapped_column(
        ForeignKey("regions.id", ondelete="CASCADE"), nullable=False
    )
    region: Mapped["Region"] = relationship(back_populates="cities")

    def __str__(self):
        return self.name


class Color(BaseModel):
    __tablename__ = "colors"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hex: Mapped[str] = mapped_column(String(50), nullable=False)
