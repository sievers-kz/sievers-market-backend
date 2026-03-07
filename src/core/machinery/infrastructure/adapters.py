from typing import Any
from uuid import UUID

from src.core.machinery.application.interfaces.attribute_validator import IAttributeValidator
from src.core.machinery.application.interfaces.wishlist_counter import IWishlistCounter
from src.core.references.application.services.attribute import AttributeService
from src.core.wishlist.application.services.wishlist import WishlistService


class AttributeValidatorAdapter(IAttributeValidator):
    def __init__(self, attribute_service: AttributeService):
        self.attribute_service = attribute_service

    async def validate(self, subcategory_id: UUID, attributes: dict[str, Any]) -> dict[str, Any]:
        return await self.attribute_service.validate(subcategory_id, attributes)


class WishlistCounterAdapter(IWishlistCounter):
    def __init__(self, wishlist_service: WishlistService):
        self.wishlist_service = wishlist_service

    async def get_total_wishlist(self, machinery_id: UUID) -> int:
        return await self.wishlist_service.count_total_wishlist(machinery_id)
