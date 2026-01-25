from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.wishlist.dto import WishlistCard
from src.core.machinery.infrastructure.models import Machinery
from src.core.references.infrastructure.models import Subcategory, City
from src.core.wishlist.application.interfaces.abstract_wishlist_repository import AbstractWishlistRepository
from src.core.wishlist.domain.entities import Wishlist as DomainWishlist
from src.core.wishlist.infrastructure.models import Wishlist as ORMWishlist


class WishlistRepository(AbstractWishlistRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._wishlist = ORMWishlist

    async def save(self, wishlist: DomainWishlist) -> None:
        mapped_model = self._wishlist(
            id=wishlist.id,
            buyer_id=wishlist.buyer_id,
            machinery_id=wishlist.machinery_id
        )
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def delete(self, buyer_id: UUID, machinery_id: UUID) -> None:
        statement = (
            delete(self._wishlist)
            .where(self._wishlist.buyer_id == buyer_id)
            .where(self._wishlist.machinery_id == machinery_id)
        )
        await self._session.execute(statement)

    async def get_by_buyer_id(self, buyer_id: UUID) -> list[WishlistCard]:
        statement = (
            select(
                Machinery.id.label("id"),
                Machinery.title.label("title"),
                Subcategory.name.label("subcategory"),
                Machinery.price.label("price"),
                Machinery.currency.label("currency"),
                City.name.label("city"),
                Machinery.created_at.label("created_at"),
            )
            .select_from(self._wishlist)
            .join(Machinery, self._wishlist.machinery_id == Machinery.id)
            .join(Subcategory, Machinery.subcategory_id == Subcategory.id)
            .join(City, Machinery.city_id == City.id)
            .where(self._wishlist.buyer_id == buyer_id)
        )

        result = await self._session.execute(statement)
        return [WishlistCard(**row) for row in result.mappings().all()]