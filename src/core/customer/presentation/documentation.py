from src.core.customer.domain.exceptions import (
    CustomerProfileRequiredError,
    FullnameRequiredError,
    InvalidFullnameFormatError,
    OrganizationAlreadyExistsError,
    OrganizationCannotBeDeletedError,
    OrganizationNotFoundError,
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

GET_CUSTOMER_ME_DOC = RouteDocs(
    operation_id="getCustomerMe",
    summary="Профиль текущего покупателя",
    description="""
        Возвращает профиль покупателя текущего аккаунта: email, ФИО и дату последней смены пароля.
        Если профиля ещё нет, он создаётся автоматически при первом обращении.
    """,
)

CREATE_ORGANIZATION_DOC = RouteDocs(
    operation_id="createOrganization",
    summary="Добавление организации",
    description="""
        Регистрирует организацию (ТОО или ИП) по ИИН/БИН и запускает фоновую проверку в госреестре.

        - `tax_id` — ровно 12 цифр, иначе `422`.
        - `kind` должен соответствовать типу налогоплательщика в реестре:
          `company` для юрлица (БИН), `individual` для ИП (ИИН).
        - Ответ приходит сразу со статусом `registry_status: pending`. Результат проверки
          (`verified` или `not_found`) нужно получать опросом `GET /organization/{organization_id}`.
        - `not_found` означает, что в реестре нет действующего налогоплательщика с таким номером и типом
          (номер не найден, тип не совпал или организация ликвидирована).
        - Если реестр временно недоступен, статус остаётся `pending`, проверка повторяется автоматически.
    """,
    responses=(OrganizationAlreadyExistsError,),
)

GET_ORGANIZATIONS_DOC = RouteDocs(
    operation_id="getOrganizations",
    summary="Список организаций покупателя",
    description="""
        Возвращает все организации текущего покупателя в порядке добавления.
        Краткий набор полей для карточек; полная информация — в `GET /organization/{organization_id}`.
    """,
)

GET_ORGANIZATION_DOC = RouteDocs(
    operation_id="getOrganization",
    summary="Организация покупателя",
    description="""
        Возвращает полную информацию об организации, включая текущий `registry_status`.
        Используется для опроса статуса после добавления организации.
        Чужая организация возвращается как ненайденная.
    """,
    responses=(OrganizationNotFoundError,),
)

DELETE_ORGANIZATION_DOC = RouteDocs(
    operation_id="deleteOrganization",
    summary="Удаление организации",
    description="""
        Безвозвратно удаляет организацию со статусом `pending` или `not_found`,
        после чего этот ИИН/БИН можно добавить заново (например, с исправленным `kind`).
        Подтверждённую (`verified`) организацию удалить нельзя.
        Чужая организация возвращается как ненайденная.
    """,
    responses=(
        OrganizationNotFoundError,
        OrganizationCannotBeDeletedError,
    ),
)
