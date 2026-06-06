from src.core.shared.domain.exceptions import NotFoundError, ValidationError


class CatalogNotFoundError(NotFoundError):
    def __init__(self, field: str):
        super().__init__(
            message="Не удалось найти объект в каталоге",
            details={"field": field}
        )


class AttributeRequiredError(ValidationError):
    def __init__(self, field: str):
        super().__init__(
            message="Пропущено обязательное поле",
            details={"field": field}
        )


class AttributeOptionError(ValidationError):
    def __init__(self):
        super().__init__(message="Некорректное значение из выпадающего списка")


class AttributeTypeError(ValidationError):
    def __init__(self, field: str):
        super().__init__(
            message="Неверный тип данных для атрибута",
            details={"field": field}
        )


class DuplicateAttributeError(ValidationError):
    def __init__(self):
        super().__init__(message="Атрибуты не должны дублироваться")