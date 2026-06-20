from enum import Enum


class MediaType(str, Enum):
    PNG = "image/png"
    JPEG = "image/jpeg"
    WEBP = "image/webp"
