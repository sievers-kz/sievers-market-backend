from src.core.shared.domain.exceptions import (
    AccessDeniedError,
    ConflictError,
    NotFoundError,
)


class InsufficientPermissionsError(AccessDeniedError):
    message = "У вас недостаточно прав доступа"
    error_code = "insufficient_permissions_error"


class AdminAlreadyExistsError(ConflictError):
    message = "Такой администратор уже зарегистрирован"
    error_code = "admin_already_exists_error"


class AdminNotFoundError(NotFoundError):
    message = "Администратор не найден"
    error_code = "admin_not_found_error"


class PermissionNotFoundError(NotFoundError):
    message = "Не удалось найти права"
    error_code = "permission_not_found_error"


class AdminProfileRequiredError(AccessDeniedError):
    message = "Для доступа требуются права администратора"
    error_code = "admin_profile_required_error"
