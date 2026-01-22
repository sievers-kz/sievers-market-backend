from uuid import UUID

from src.core.machinery.application.interfaces.abstract_machinery_reader import AbstractMachineryReader


class GetOwnerDetailMachineryUseCase:
    def __init__(self, reader: AbstractMachineryReader):
        self.reader = reader

    async def execute(self, machinery_id: UUID, seller_id: UUID):
        return await self.reader.get_owner_detail_machinery(machinery_id, seller_id)
