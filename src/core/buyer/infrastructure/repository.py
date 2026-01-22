from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.buyer.application.interfaces.abstract_buyer_repository import AbstractBuyerRepository
from src.core.buyer.infrastructure.mapper import BuyerMapper
from src.core.buyer.infrastructure.models import Buyer as ORMBuyer
from src.core.buyer.domain.entities import Buyer as DomainBuyer


class BuyerRepository(AbstractBuyerRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._model = ORMBuyer

    async def save(self, buyer: DomainBuyer) -> None:
        mapped_model = BuyerMapper.to_orm(buyer)
        await self._session.merge(mapped_model)
        await self._session.flush()

    async def get_by_account_id(self, account_id: UUID) -> DomainBuyer:
        statement = (
            select(self._model)
            .where(self._model.account_id == account_id)
        )

        query_result = await self._session.execute(statement)
        orm_model = query_result.scalar_one_or_none()

        if orm_model is None:
            return None

        return BuyerMapper.to_domain(orm_model)
