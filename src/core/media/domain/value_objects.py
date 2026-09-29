from dataclasses import dataclass

from src.core.media.domain.exceptions import (
    MediaSizeError,
)


@dataclass(frozen=True)
class MediaSize:
    MAX_SIZE_BYTES = 20 * 1024 * 1024
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise MediaSizeError()
        if self.value > self.MAX_SIZE_BYTES:
            raise MediaSizeError()
