from uuid import UUID

from src.core.customer.application.interfaces.abstract_customer_service import AbstractCustomerService
from src.core.iam.application.interfaces.abstract_profile_creator import AbstractProfileCreator


class ProfileCreatorAdapter(AbstractProfileCreator):
    def __init__(self, customer_service: AbstractCustomerService):
        self.customer_service = customer_service

    async def create(self, account_id: UUID, last_name: str, first_name: str):
        await self.customer_service.create(account_id, last_name, first_name)
