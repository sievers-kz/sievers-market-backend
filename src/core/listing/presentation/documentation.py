from src.core.customer.domain.exceptions import OrganizationCannotPublishError, OrganizationNotFoundError
from src.core.listing.domain.exceptions import (
    ListingDeletedError,
    ListingInvalidFilterKeyError,
    ListingNotFoundError,
)
from src.core.shared.presentation.documentation import RouteDocs

CREATE_LISTING_DOC = RouteDocs(
    operation_id="createListing",
    summary="Создание объявления",
    description="""
        Создаёт новое объявление со статичными полями, галереей и динамическими атрибутами подкатегории.

        Объявление размещается от имени организации из `organization_id`. Организация должна принадлежать
        текущему покупателю (иначе `404`) и быть подтверждённой в реестре, `registry_status: verified`
        (иначе `403`). Список организаций для выбора — `GET /api/v1/customer/organizations`.
    """,
    responses=(
        OrganizationNotFoundError,
        OrganizationCannotPublishError,
    ),
)

CHANGE_LISTING_PRICE_DOC = RouteDocs(
    operation_id="changeListingPrice",
    summary="Изменение цены объявления",
    description="""
        Обновляет цену и валюту объявления.
    """,
    responses=(ListingNotFoundError,),
)

CHANGE_LISTING_LOCATION_DOC = RouteDocs(
    operation_id="changeListingLocation",
    summary="Изменение локации объявления",
    description="""
        Обновляет город объявления.
    """,
    responses=(ListingNotFoundError,),
)

CHANGE_LISTING_DESCRIPTION_DOC = RouteDocs(
    operation_id="changeListingDescription",
    summary="Изменение описания объявления",
    description="""
        Обновляет текстовое описание объявления.
    """,
    responses=(ListingNotFoundError,),
)

CHANGE_LISTING_ATTRIBUTE_DOC = RouteDocs(
    operation_id="changeListingAttribute",
    summary="Изменение атрибутов объявления",
    description="""
        Обновляет значения динамических атрибутов объявления в рамках подкатегории.
    """,
    responses=(ListingNotFoundError,),
)

ACTIVATE_LISTING_DOC = RouteDocs(
    operation_id="activateListing",
    summary="Публикация объявления",
    description="""
        Переводит объявление в статус `active` — делает его видимым в публичном каталоге.
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

DEACTIVATE_LISTING_DOC = RouteDocs(
    operation_id="deactivateListing",
    summary="Снятие объявления с публикации",
    description="""
        Переводит объявление в статус `inactive` — скрывает из каталога без удаления.
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

ARCHIVE_LISTING_DOC = RouteDocs(
    operation_id="archiveListing",
    summary="Архивация объявления",
    description="""
        Переводит объявление в статус `archived`.
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

DELETE_LISTING_DOC = RouteDocs(
    operation_id="deleteListing",
    summary="Удаление объявления",
    description="""
        Переводит объявление в статус `deleted` (мягкое удаление).
    """,
    responses=(
        ListingNotFoundError,
        ListingDeletedError,
    ),
)

SEARCH_LISTING_DOC = RouteDocs(
    operation_id="searchListing",
    summary="Поиск объявлений",
    description="""
        Полнотекстовый поиск объявлений через Meilisearch с фильтрами и пагинацией.
    """,
    responses=(ListingInvalidFilterKeyError,),
)

GET_LISTINGS_CATALOG_DOC = RouteDocs(
    operation_id="getListingsCatalog",
    summary="Список объявлений каталога",
    description="""
        Возвращает постраничный список карточек объявлений по категории/подкатегории.
    """,
    responses=(),
)

GET_LISTING_DETAILS_DOC = RouteDocs(
    operation_id="getListingDetails",
    summary="Детали объявления",
    description="""
        Возвращает полную карточку объявления: владелец, галерея, динамические атрибуты.
    """,
    responses=(ListingNotFoundError,),
)
