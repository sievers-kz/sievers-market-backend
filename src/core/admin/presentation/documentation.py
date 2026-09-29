from src.core.admin.domain.exceptions import (
    AdminAlreadyExistsError,
    InsufficientPermissionsError,
    PermissionNotFoundError,
)
from src.core.iam.domain.exceptions import AccountNotFoundError
from src.core.shared.presentation.documentation import RouteDocs

CREATE_ADMIN_DOC = RouteDocs(
    operation_id="createAdmin",
    summary="Создание админ-аккаунта",
    description="""
        Создаёт учётную запись администратора.
    """,
    responses=(
        AccountNotFoundError,
        AdminAlreadyExistsError,
        InsufficientPermissionsError,
    ),
)

GRANT_PERMISSION_DOC = RouteDocs(
    operation_id="grantPermission",
    summary="Выдача прав администратору",
    description="""
        Выдаёт администратору право (`action:resource` codename) через RBAC/PBAC.
    """,
    responses=(
        InsufficientPermissionsError,
        PermissionNotFoundError,
    ),
)
