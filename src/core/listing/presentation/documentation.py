from src.core.catalog.infrastructure.exceptions import CatalogNotFoundError
from src.core.customer.domain.exceptions import (
    OrganizationCannotPublishError,
    OrganizationNotFoundError,
    OrganizationProfileIncompleteError,
)
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

        Категория должна существовать, а подкатегория — принадлежать этой категории, иначе `404`
        `catalog_not_found_error` (`metadata.field` — id не найденного объекта). Подкатегория без
        заданных атрибутов допустима.
    """,
    responses=(
        OrganizationNotFoundError,
        CatalogNotFoundError,
        OrganizationCannotPublishError,
        OrganizationProfileIncompleteError,
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

        `subcategory_id` должен совпадать с подкатегорией объявления, иначе `404` `catalog_not_found_error`.
    """,
    responses=(
        ListingNotFoundError,
        CatalogNotFoundError,
    ),
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
        Возвращает постраничный список карточек объявлений по категории/подкатегории, сначала новые.
        В карточке: дата создания (`created_at`), название организации-продавца (`organization_name`:
        название магазина или, если его нет, юридическое название) и состояние (`condition`: `new` или `used`;
        `null`, если у подкатегории нет такого атрибута).
    """,
    responses=(),
)

GET_MY_LISTINGS_DOC = RouteDocs(
    operation_id="getMyListings",
    summary="Мои объявления",
    description="""
        Возвращает постраничный список объявлений всех организаций текущего покупателя (кабинет).

        Читает из базы, а не из поискового индекса, поэтому видны и неактивные объявления. Удалённые не
        возвращаются. Без `status` приходят активные, неактивные и архивные.

        Фильтры: `status` (`active`, `inactive`, `archived`), `organization_id` (организация должна
        принадлежать текущему покупателю, иначе `404`), `category_id`. Сортировка `sort`: `newest`
        (по умолчанию) или `oldest` по дате создания. `limit` от 1 до 50.

        `preview_image` и `city` могут быть `null` (нет фото или города).
    """,
    responses=(OrganizationNotFoundError,),
)

GET_LISTING_DETAILS_DOC = RouteDocs(
    operation_id="getListingDetails",
    summary="Детали объявления",
    description="""
        Возвращает полную карточку объявления: владелец, галерея, динамические атрибуты.
    """,
    responses=(ListingNotFoundError,),
)
