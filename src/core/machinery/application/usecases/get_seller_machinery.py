from uuid import UUID

from src.core.machinery.application.interfaces.abstract_machinery_reader import AbstractMachineryReader
from src.core.machinery.domain.enums import ListingStatus


class GetSellerMachineryUseCase:
    def __init__(self, reader: AbstractMachineryReader):
        self.reader = reader

    async def execute(self, seller_id: UUID, status: ListingStatus, page: int, limit: int):
        return await self.reader.get_seller_machinery(seller_id, status, page, limit)
