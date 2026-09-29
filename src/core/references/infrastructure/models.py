from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.shared.infrastructure.base_model import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class OriginCountry(BaseModel):
    __tablename__ = "origin_countries"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class City(BaseModel):
    __tablename__ = "cities"
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Color(BaseModel):
    __tablename__ = "colors"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    hex: Mapped[str] = mapped_column(String(50), nullable=False)
