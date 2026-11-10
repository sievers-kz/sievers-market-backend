from src.core.shared.domain.exceptions import (
    AccessDeniedError,
    ConflictError,
    NotFoundError,
    RulesError,
    ValidationError,
)


class CustomerNotFoundError(NotFoundError):
    message = "Не удалось найти профиль покупателя"
    error_code = "customer_not_found_error"


class FullnameRequiredError(ValidationError):
    message = "Обязательное поле не заполнено"
    error_code = "fullname_required_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})


class InvalidFullnameFormatError(ValidationError):
    message = "Неверный формат поля"
    error_code = "invalid_fullname_format_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})


class CustomerProfileRequiredError(AccessDeniedError):
    message = "Доступ запрещен. Необходимо иметь профиль покупателя"
    error_code = "customer_profile_required_error"


class TaxpayerNotFoundError(NotFoundError):
    message = "Не удалось найти такую организацию"
    error_code = "taxpayer_not_found_error"


class OrganizationAlreadyExistsError(ConflictError):
    message = "Такая организация уже зарегистрирована"
    error_code = "organization_already_exists_error"


class OrganizationOwnershipLimitError(RulesError):
    message = "У вас не может быть больше одной организации"
    error_code = "organization_ownership_limit_error"


class OrganizationRequiredError(AccessDeniedError):
    message = "Требуется организация"
    error_code = "organization_required_error"


class OrganizationNotFoundError(NotFoundError):
    message = "Не удалось найти такую организацию"
    error_code = "organization_not_found_error"


class TaxpayerRegistryUnavailableError(Exception):
    pass


class OrganizationCannotBeDeletedError(RulesError):
    message = "Нельзя удалить активную организацию"
    error_code = "organization_cannot_be_deleted"
