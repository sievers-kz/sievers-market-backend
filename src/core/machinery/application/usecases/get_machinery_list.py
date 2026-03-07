from src.core.machinery.application.interfaces.query import IMachineryQuery
from src.core.machinery.presentation.filters import MachineryFilter


class GetMachineryListUseCase:
    def __init__(self, query: IMachineryQuery):
        self.query = query

    async def execute(self, filters: MachineryFilter, page: int, limit: int):
        return await self.query.get_machinery_list(filters, page, limit)
