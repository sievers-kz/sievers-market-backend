import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, func, Text, Boolean, Integer, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.configuration.database.connection import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    type_annotation_map = {
        enum.Enum: Enum(
            enum.Enum,  # Абстрактный маркер
            native_enum=False,  # Отключает родные Enum базы данных (будет VARCHAR)
            # Заставляет SQLAlchemy динамически брать .value конкретного энума
            values_callable=lambda obj: [item.value for item in obj],
        )
    }


