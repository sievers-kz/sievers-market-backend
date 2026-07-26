from uuid import UUID

from sqlalchemy import UUID as ORMUUID
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.media.domain.enums import MediaType
from src.core.shared.infrastructure.base_model import BaseModel


class Media(BaseModel):
    __tablename__ = "media"

    owner_id: Mapped[UUID] = mapped_column(ORMUUID, nullable=False)
    media_url: Mapped[str] = mapped_column(String, nullable=False)
    media_type: Mapped[MediaType] = mapped_column(nullable=False)
    media_size: Mapped[int] = mapped_column(Integer, nullable=False)
