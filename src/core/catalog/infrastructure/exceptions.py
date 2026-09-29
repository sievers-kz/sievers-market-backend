from src.core.shared.domain.exceptions import ConflictError, NotFoundError


class CatalogNotFoundError(NotFoundError):
    message = "Не удалось найти объект в каталоге"
    error_code = "catalog_not_found_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})


class AttributeAlreadyAttachedError(ConflictError):
    message = "Атрибут уже привязан к этой категории"
    error_code = "attribute_already_attached_error"

    def __init__(self, subcategory_id: str, attribute_id: str):
        super().__init__(
            message=self.message,
            metadata={"subcategory_id": subcategory_id, "attribute_id": attribute_id},
        )


class CatalogItemNotFoundError(NotFoundError):
    message = "Не удалось найти объект в каталоге"
    error_code = "catalog_item_not_found_error"

    def __init__(self, field: str):
        super().__init__(message=self.message, metadata={"field": field})
