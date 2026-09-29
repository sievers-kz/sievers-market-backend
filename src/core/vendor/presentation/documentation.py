from src.core.shared.domain.exceptions import InvalidPhoneFormatError
from src.core.shared.presentation.documentation import RouteDocs
from src.core.vendor.domain.exceptions import (
    ContactFullnameFormatError,
    ContactFullnameRequiredError,
    InvalidLogotypeSizeError,
    TaxpayerNotFoundError,
    TaxpayerOnLiquidationError,
    VendorAlreadyExistsError,
    VendorCannotBeRestoredError,
    VendorNotFoundError,
    VendorProfileRequiredError,
)

VERIFY_TAXPAYER_DOC = RouteDocs(
    operation_id="verifyTaxpayer",
    summary="Проверка налогоплательщика по ИИН / БИН",
    description="""
        Проверяет `ИИН` & `БИН` во внешнем реестре налогоплательщиков и возвращает:
        * Юридическое наименование
        * Организационно-правовую форму (ОПФ)
        * Статус ликвидации
        Первый шаг онбординга продавца.
    """,
    responses=(
        TaxpayerOnLiquidationError,
        TaxpayerNotFoundError,
    ),
)

CREATE_VENDOR_DOC = RouteDocs(
    operation_id="createVendor",
    summary="Создание профиля продавца",
    description="""
        Заводит профиль продавца для текущего аккаунта на основе проверенных данных налогоплательщик
    """,
    responses=(
        TaxpayerOnLiquidationError,
        TaxpayerNotFoundError,
        VendorAlreadyExistsError,
    ),
)

CHANGE_CONTACT_FULLNAME_DOC = RouteDocs(
    operation_id="changeContactFullname",
    summary="Изменение ФИО контактного лица",
    description="""
        Обновляет ФИО контактного лица продавца.
    """,
    responses=(
        VendorProfileRequiredError,
        ContactFullnameRequiredError,
        ContactFullnameFormatError,
    ),
)

CHANGE_CONTACT_PHONE_DOC = RouteDocs(
    operation_id="changeContactPhone",
    summary="Изменение контактного телефона",
    description="""
        Обновляет контактный телефон продавца.
    """,
    responses=(
        VendorProfileRequiredError,
        InvalidPhoneFormatError,
    ),
)

CHANGE_SHOP_NAME_DOC = RouteDocs(
    operation_id="changeShopName",
    summary="Изменение названия магазина",
    description="""
        Обновляет публичное название магазина продавца.
    """,
    responses=(VendorProfileRequiredError,),
)

CHANGE_LOGOTYPE_DOC = RouteDocs(
    operation_id="changeLogotype",
    summary="Изменение логотипа магазина",
    description="""
        Обновляет логотип магазина; принимает медиа-объект, ранее загруженный через `/api/v1/media`.
    """,
    responses=(
        VendorProfileRequiredError,
        InvalidLogotypeSizeError,
    ),
)

GET_ME_LISTINGS_DOC = RouteDocs(
    operation_id="getMeListings",
    summary="Мои объявления по статусу",
    description="""
        Возвращает постраничный список объявлений текущего продавца, отфильтрованных по статусу
        (`active`, `inactive`, `archived`, `deleted`).
    """,
    responses=(VendorProfileRequiredError,),
)

CLOSE_VENDOR_DOC = RouteDocs(
    operation_id="closeVendor",
    summary="Закрытие профиля продавца",
    description="""
        Деактивирует профиль продавца — витрина и объявления скрываются из публичного каталога.
    """,
    responses=(VendorProfileRequiredError,),
)

RESTORE_VENDOR_DOC = RouteDocs(
    operation_id="restoreVendor",
    summary="Восстановление профиля продавца",
    description="""
        Восстанавливает ранее закрытый профиль продавца.
        Восстановление возможно только **в течении 30 дней** с момента закрытия.
        По истечению более 30 дней, профиль считается окончательно удаленным.
    """,
    responses=(VendorCannotBeRestoredError,),
)

GET_VENDOR_CATALOG_DOC = RouteDocs(
    operation_id="getVendorCatalog",
    summary="Каталог продавцов",
    description="""
        Возвращает постраничный публичный список карточек продавцов.
        Продавцы не прошедшие верификацию не отображаются в публичном каталоге продавцов.
    """,
    responses=(),
)

GET_VENDOR_DETAILS_DOC = RouteDocs(
    operation_id="getVendorDetails",
    summary="Детали продавца",
    description="""
        Возвращает публичную карточку продавца с полной информацией: реквизиты, логотип, статус верификации.
    """,
    responses=(VendorNotFoundError,),
)
