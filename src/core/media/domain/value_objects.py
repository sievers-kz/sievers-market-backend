from dataclasses import dataclass

from src.core.media.domain.exceptions import MediaImageTooLargeError, InvalidMediaSizeError


@dataclass(frozen=True)
class MediaSize:
    MAX_SIZE_BYTES = 20 * 1024 * 1024
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise InvalidMediaSizeError()
        if self.value > self.MAX_SIZE_BYTES:
            raise MediaImageTooLargeError()
