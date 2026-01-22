from src.api.iam.dto import AccountConfirmation
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork


class AccountConfirmationUseCase:
    def __init__(self, unit_of_work: AbstractIAMUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, confirmation_data: AccountConfirmation):
        async with self.unit_of_work as uow:
            account = await uow.account.find_by_token_value(confirmation_data.confirm_token)
            if not account:
                raise ValueError("Invalid confirmation token")

            account.confirm_account()
            account.revoke_token(confirmation_data.confirm_token)

            await uow.account.save(account)
            await uow.commit()
