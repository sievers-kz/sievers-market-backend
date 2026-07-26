from src.core.shared.domain.exceptions import NotFoundError, ValidationError


class CatalogNotFoundError(NotFoundError):
    def __init__(self, field: str):
        super().__init__(
            message="Не удалось найти объект в каталоге", details={"field": field}
        )


class AttributeAlreadyAttachedError(ValidationError):
    def __init__(self, subcategory_id: str, attribute_id: str):
        super().__init__(
            message="Атрибут уже привязан к этой подкатегории",
            details={"subcategory_id": subcategory_id, "attribute_id": attribute_id},
        )
