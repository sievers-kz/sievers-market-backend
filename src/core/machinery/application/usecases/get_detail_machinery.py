from uuid import UUID

from src.core.machinery.application.interfaces.query import IMachineryQuery


class GetMachineryDetailUseCase:
    def __init__(self, query: IMachineryQuery):
        self.query = query

    async def execute(self, machinery_id: UUID):
        return await self.query.get_machinery_detail(machinery_id)
