from uuid import UUID

from src.core.iam.application.interfaces.password_service import IPasswordService
from src.core.iam.domain.exceptions import PasswordMismatchError, AccountNotFoundError
from src.core.iam.presentation.dto import ChangePasswordData
from src.core.iam.application.interfaces.uow import IIAMUnitOfWork


class ChangePasswordUseCase:
    def __init__(
        self,
        unit_of_work: IIAMUnitOfWork,
        password_service: IPasswordService
    ):
        self.unit_of_work = unit_of_work
        self.password_service = password_service

    async def execute(self, account_id: UUID, change_password_data: ChangePasswordData):
        async with self.unit_of_work as uow:
            account = await uow.account.get_account_by_id(account_id)

            self.password_service.validate(change_password_data.new_password)
            if not self.password_service.verify(change_password_data.raw_password, account.password.value):
                raise PasswordMismatchError()

            new_hashed_password = self.password_service.hash(change_password_data.new_password)
            account.change_password(new_hashed_password)

            await uow.account.save(account)
            await uow.commit()
