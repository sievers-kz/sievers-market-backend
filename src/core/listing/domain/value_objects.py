from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class Image:
    MAX_SIZE_BYTES = 5 * 1024 * 1024
    media_id: UUID
    media_type: str
    media_size: int

    def __post_init__(self):
        # TODO: Реализовать валидацию бизнес-инвариантов изображения:
        # 1. Проверить, что разрешение не меньше NxN и не больше N.
        # 3. Валидировать формат (допускать только jpeg, png, webp).
        if self.media_size > self.MAX_SIZE_BYTES:
            raise ValueError("Изображение не может превышать 5 МБ")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Image":
        return cls(
            media_id=UUID(str(data["media_id"])),
            media_type=data["media_type"],
            media_size=int(data["media_size"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "media_id": str(self.media_id),
            "media_type": str(self.media_type),
            "media_size": int(self.media_size),
        }


@dataclass(frozen=True)
class Gallery:
    images: tuple[Image, ...]

    def __post_init__(self):
        if not self.images:
            raise ValueError("Добавьте минимум одно изображение")
        if len(self.images) > 10:
            raise ValueError("Вы можете добавить максимум 10 изображений")

    @classmethod
    def from_dicts(cls, data: list[dict[str, Any]]) -> "Gallery":
        return cls(images=tuple(Image.from_dict(item) for item in data))

    def to_dicts(self) -> list[dict[str, Any]]:
        return [image.to_dict() for image in self.images]
