from src.core.shared.domain.exceptions import ValidationError


class MediaImageTooLargeError(ValidationError):
    def __init__(self):
        super().__init__(message="Размер изображения слишком велик. Допустимо до 20 МБ")
        

class InvalidMediaSizeError(ValidationError):
    def __init__(self):
        super().__init__(message="Размер файла должен быть больше нуля")