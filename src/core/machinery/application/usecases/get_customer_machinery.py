from uuid import UUID

from src.core.machinery.application.interfaces.query import IMachineryQuery
from src.core.machinery.presentation.filters import MachineryOwnerFilter


class GetCustomerMachineryUseCase:
    def __init__(self, query: IMachineryQuery):
        self.query = query

    async def execute(self, customer_id: UUID, filters: MachineryOwnerFilter, page: int, limit: int):
        return await self.query.get_customer_machinery(customer_id, filters, page, limit)

