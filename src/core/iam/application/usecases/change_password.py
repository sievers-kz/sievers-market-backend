from uuid import UUID

from src.api.iam.dto import ChangePasswordData
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork
from src.core.shared.infrastructure.services.password_hasher import AbstractPasswordHasher


class ChangePasswordUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        password_hasher: AbstractPasswordHasher
    ):
        self.unit_of_work = unit_of_work
        self.password_hasher = password_hasher

    async def execute(self, account_id: UUID, change_password_data: ChangePasswordData):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_id(account_id)
            if not account:
                raise ValueError("Account not found")

            new_password_hash = self.password_hasher.hash_password(change_password_data.new_password)
            account.change_password(change_password_data.raw_password, new_password_hash, self.password_hasher)

            await uow.account.save(account)
            await uow.commit()
