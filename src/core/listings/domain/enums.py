from enum import Enum


class ListingCurrencyEnum(Enum):
    KZT = "KZT"
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"


class ListingStatusEnum(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"


class MimeTypeEnum(Enum):
    JPEG = "image/jpeg"
    PNG = "image/png"
    WEBP = "image/webp"


class MachineryConditionEnum(Enum):
    USED = "used"
    NEW = "new"



