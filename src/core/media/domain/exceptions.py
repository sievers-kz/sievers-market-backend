from src.core.shared.domain.exceptions import NotFoundError, ValidationError


class MediaSizeError(ValidationError):
    message = "Размер изображения должен быть не меньше 0 и не больше 20 MB"
    error_code = "media_size_error"


class MediaNotFoundError(NotFoundError):
    message = "Не удалось найти изображение"
    error_code = "media_not_found_error"
