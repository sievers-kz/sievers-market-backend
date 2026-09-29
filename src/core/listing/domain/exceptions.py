from src.core.shared.domain.exceptions import (
    AccessDeniedError,
    ConflictError,
    NotFoundError,
    RulesError,
    ValidationError,
)


class ListingNotFoundError(NotFoundError):
    message = "Не удалось найти объявление"
    error_code = "listing_not_found_error"


class ListingLargeImageSizeError(ValidationError):
    message = "Изображение слишком велико. Максимум 5 MB"
    error_code = "listing_large_image_error"


class ListingGallerySizeError(ValidationError):
    message = "Количество изображений должно быть от 1 до 10"
    error_code = "listing_gallery_size_error"

    def __init__(self, count: int):
        super().__init__(message=self.message, metadata={"count": count, "min": 1, "max": 10})


class ListingActivationError(RulesError):
    message = "Невозможно активировать объявление"
    error_code = "listing_activation_error"


class ListingArchivingError(RulesError):
    message = "Невозможно архивировать объявление"
    error_code = "listing_archiving_error"


class ListingDeletedError(ConflictError):
    message = "Объявление удалено. Чтобы изменить статус, сначала восстановите его"
    error_code = "listing_deleted_error"


class ListingAccessDeniedError(AccessDeniedError):
    message = "Вы не являетесь владельцем этого объявления"
    error_code = "listing_access_denied_error"
