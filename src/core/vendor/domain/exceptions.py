from src.core.shared.domain.exceptions import (
    AccessDeniedError,
    ConflictError,
    NotFoundError,
    RulesError,
    ValidationError,
)


class VendorNotFoundError(NotFoundError):
    message = "Не удалось найти профиль продавца"
    error_code = "vendor_not_found_error"


class TaxpayerNotFoundError(NotFoundError):
    message = "Не удалось найти организацию"
    error_code = "taxpayer_not_found_error"


class TaxpayerOnLiquidationError(RulesError):
    message = "Данная организация находится на ликвидации"
    error_code = "taxpayer_on_liquidation_error"


class VendorAlreadyExistsError(ConflictError):
    message = "Такой продавец уже зарегистрирован в системе"
    error_code = "vendor_already_exists_error"


class ContactFullnameRequiredError(ValidationError):
    message = "Обязательное поле не заполнено"
    error_code = "contact_fullname_required_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})


class ContactFullnameFormatError(ValidationError):
    message = "Неправильный формат поля"
    error_code = "contact_fullname_format_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})


class InvalidTaxNumberError(ValidationError):
    message = "Некорректный формат идентификационного номера"
    error_code = "invalid_tax_number_error"


class InvalidLogotypeSizeError(ValidationError):
    message = "Размер логотипа не должен превышать 2МB"
    error_code = "invalid_logotype_size_error"


class VendorAlreadyVerifiedError(ConflictError):
    message = "Продавец уже верифицирован"
    error_code = "vendor_already_verified_error"


class VendorCannotBeRestoredError(RulesError):
    message = "Невозможно восстановить аккаунт продавца"
    error_code = "vendor_cannot_be_restored_error"


class VendorProfileRequiredError(AccessDeniedError):
    message = "Доступ запрещен. Необходимо иметь профиль продавца"
    error_code = "vendor_profile_required_error"
