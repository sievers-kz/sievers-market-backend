from src.core.customer.domain.exceptions import (
    CustomerProfileRequiredError,
    FullnameRequiredError,
    InvalidFullnameFormatError,
)
from src.core.shared.presentation.documentation import RouteDocs

CREATE_CUSTOMER_DOC = RouteDocs(
    operation_id="createCustomer",
    summary="Создание профиля покупателя",
    description="""
        Заводит профиль покупателя для текущего аккаунта — часть онбординга после регистрации.
    """,
    responses=(
        FullnameRequiredError,
        InvalidFullnameFormatError,
    ),
)

CHANGE_CUSTOMER_FULLNAME_DOC = RouteDocs(
    operation_id="changeCustomerFullname",
    summary="Изменение ФИО покупателя",
    description="""
        Обновляет фамилию, имя и отчество в профиле покупателя.
    """,
    responses=(
        CustomerProfileRequiredError,
        FullnameRequiredError,
        InvalidFullnameFormatError,
    ),
)
