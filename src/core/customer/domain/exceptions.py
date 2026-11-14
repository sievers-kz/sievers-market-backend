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


class OrganizationCannotPublishError(AccessDeniedError):
    message = "Организация ещё не подтверждена и не может размещать объявления"
    error_code = "organization_cannot_publish_error"


class OrganizationProfileIncompleteError(AccessDeniedError):
    message = "Дополните данные организации, чтобы размещать объявления"
    error_code = "organization_profile_incomplete_error"

    def __init__(self, missing_fields: list[str]):
        super().__init__(message=self.message, metadata={"missing_fields": missing_fields})


class InvalidShopNameError(ValidationError):
    message = "Название магазина должно содержать от 2 до 50 символов и хотя бы одну букву"
    error_code = "invalid_shop_name_error"

    def __init__(self):
        super().__init__(message=self.message, metadata={"field": "shop_name"})
