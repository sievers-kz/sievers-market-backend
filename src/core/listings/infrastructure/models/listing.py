from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Integer, Enum, Text, Boolean, DateTime, Index, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.listings.domain.enums import ListingCurrencyEnum, ListingStatusEnum, MimeTypeEnum
from src.core.shared.infrastructure.base_model import BaseModel

if TYPE_CHECKING:
    from src.core.users.infrastructure.models import User
    from src.core.references.infrastructure.models import Roubric
    from src.core.references.infrastructure.models import Region
    from src.core.listings.infrastructure.models.machinery import Machinery


class Listing(BaseModel):
    __tablename__ = "listings"

    author_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        )
    )

    roubric_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roubrics.id",
            ondelete="CASCADE"
        )
    )

    region_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "regions.id",
            ondelete="CASCADE"
        )
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    currency: Mapped[ListingCurrencyEnum] = mapped_column(
        Enum(ListingCurrencyEnum),
        nullable=False,
        default=ListingCurrencyEnum.KZT.value
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[ListingStatusEnum] = mapped_column(
        Enum(ListingStatusEnum),
        nullable=False,
        default=ListingStatusEnum.DRAFT.value
    )

    author: Mapped["User"] = relationship(
        back_populates="listings",
    )

    roubric: Mapped["Roubric"] = relationship(
        back_populates="listings",
    )

    region: Mapped["Region"] = relationship(
        back_populates="listings",
    )

    media: Mapped[list["ListingMedia"]] = relationship(
        back_populates="listing",
        cascade="all, delete-orphan",
        order_by="ListingMedia.position",
        lazy="selectin",
    )

    machinery: Mapped["Machinery | None"] = relationship(
        back_populates="listing"
    )

    __table_args__ = (
        Index("ix_listings_author", "author_id"),
        Index("ix_listings_roubric", "roubric_id"),
        Index("ix_listings_region", "region_id"),
        Index("ix_listings_status", "status")
    )


class ListingMedia(BaseModel):
    __tablename__ = "listing_media"

    listing_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "listings.id",
            ondelete="CASCADE"
        )
    )

    media_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    mime_type: Mapped[MimeTypeEnum] = mapped_column(
        Enum(MimeTypeEnum),
        nullable=False,
    )

    is_main: Mapped[bool] = mapped_column(
        Boolean,
        server_default="false",
        default=False
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    listing: Mapped["Listing"] = relationship(
        back_populates="media"
    )

    __table_args__ = (
        Index(
            "uq_listing_media_one_main",
            "listing_id",
            unique=True,
            postgresql_where=text("is_main = true")  # ← Оберни в text()
        ),
        Index("ix_listing_media_listing_id", "listing_id"),
        Index("ix_listing_media_listing_position", "listing_id", "position")
    )
