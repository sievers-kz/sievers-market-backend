from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.core.media.domain.enums import MediaType
from src.core.shared.infrastructure.base_model import BaseModel


class Media(BaseModel):
    __tablename__ = "media"

    machinery_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "machinery.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    media_url: Mapped[str] = mapped_column(String, nullable=False)

    media_type: Mapped[MediaType] = mapped_column(
        Enum(
            MediaType,
            native_enum=False,
            values_callable=BaseModel.get_enum_values
        ),
        nullable=False
    )

    media_size: Mapped[int] = mapped_column(Integer, nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
