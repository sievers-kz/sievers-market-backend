import enum

from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    type_annotation_map = {
        enum.Enum: Enum(
            enum.Enum,  # Абстрактный маркер
            native_enum=False,  # Отключает родные Enum базы данных (будет VARCHAR)
            # Заставляет SQLAlchemy динамически брать .value конкретного энума
            values_callable=lambda obj: [item.value for item in obj],
        )
    }
