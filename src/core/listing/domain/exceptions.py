from src.core.shared.domain.exceptions import NotFoundError, RulesError, ValidationError


class ListingNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(message="Не удалось найти объявление")


class ListingLargeImageSizeError(ValidationError):
    def __init__(self):
        super().__init__(message="Изображение слишком велико. Максимум 5 МБ")


class ListingGalleryEmptyError(ValidationError):
    def __init__(self):
        super().__init__(
            message="Объявление должно содержать как минимум 1 изображение"
        )


class ListingGalleryTooManyImagesError(ValidationError):
    def __init__(self):
        super().__init__(message="Можно добавить только до 10 изображений")


class ListingActivationError(RulesError):
    def __init__(self):
        super().__init__(message="Невозможно активировать удаленное объявление")


class ListingArchivingError(ValidationError):
    def __init__(self):
        super().__init__(message="Невозможно архивировать удаленное объявление")
