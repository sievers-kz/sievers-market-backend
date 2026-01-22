from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.seller.application.interfaces.abstract_seller_repository import AbstractSellerRepository
from src.core.seller.domain.entities import Seller as DomainSeller
from src.core.seller.infrastructure.mapper import SellerMapper
from src.core.seller.infrastructure.models import Seller as ORMSeller


class SellerRepository(AbstractSellerRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._model = ORMSeller

    async def save(self, seller: DomainSeller) -> None:
        mapped_model = SellerMapper.to_orm(seller)
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def get_by_account_id(self, account_id: UUID) -> DomainSeller:
        statement = (
            select(self._model)
            .where(self._model.account_id == account_id)
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.scalar_one_or_none()

        if orm_model is None:
            return None

        return SellerMapper.to_domain(orm_model)
