from uuid import UUID

from src.core.customer.infrastructure.repository import CustomerRepository


class ListingLimitService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository

    async def can_create(self, owner_id: UUID):
        customer = await self.customer_repository.get_by_account_id(owner_id)
        if customer:
            return customer
        raise ValueError("User not found")
