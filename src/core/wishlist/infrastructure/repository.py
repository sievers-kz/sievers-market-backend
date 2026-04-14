from uuid import UUID

from sqlalchemy import delete, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.wishlist.presentation.dto import WishlistCard
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
            customer_id=wishlist.customer_id,
            machinery_id=wishlist.machinery_id
        )
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def delete(self, customer_id: UUID, machinery_id: UUID) -> None:
        statement = (
            delete(self._wishlist)
            .where(self._wishlist.customer_id == customer_id)
            .where(self._wishlist.machinery_id == machinery_id)
        )
        await self._session.execute(statement)

    async def get_by_customer_id(self, customer_id: UUID) -> list[WishlistCard]:
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
            .where(self._wishlist.customer_id == customer_id)
        )

        result = await self._session.execute(statement)
        return [WishlistCard(**row) for row in result.mappings().all()]

    async def count_total_wishlist(self, machinery_id: UUID) -> int:
        statement = (
            select(func.count())
            .select_from(self._wishlist)
            .where(
                self._wishlist.machinery_id == machinery_id,
            )
        )

        return await self._session.scalar(statement)
