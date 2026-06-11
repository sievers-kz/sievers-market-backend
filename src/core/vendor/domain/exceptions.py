from src.core.shared.domain.exceptions import NotFoundError, RulesError, AlreadyExistsError, ValidationError


class VendorNotFoundError(NotFoundError):
    def __init__(self):
        super().__init__(message="Не удалось найти такого продавца")


class VendorOnLiquidationError(RulesError):
    def __init__(self):
        super().__init__(message="Данный продавец находится на ликвидации")


class VendorAlreadyExistsError(AlreadyExistsError):
    def __init__(self):
        super().__init__(message="Такой продавец уже зарегистрирован в системе")


class ContactFullnameRequiredError(ValidationError):
    def __init__(self, field: str):
        super().__init__(
            message="Обязательное поле не заполнено",
            details={"field": field}
        )


class ContactFullnameFormatError(ValidationError):
    def __init__(self, field: str):
        super().__init__(
            message="Неправильный формат поля",
            details={"field": field}
        )


class InvalidTaxNumberError(ValidationError):
    def __init__(self):
        super().__init__(message="Некорректный формат ИН")


class InvalidLogotypeSizeError(ValidationError):
    def __init__(self):
        super().__init__(message="Размер логотипа не должен превышать 2 МБ")


class VendorAlreadyVerifiedError(RulesError):
    def __init__(self):
        super().__init__(message="Продавец уже верифицирован")


class VendorCannotBeRestoredError(ValidationError):
    def __init__(self):
        super().__init__(message="Невозможно восстановить аккаунт продавца")