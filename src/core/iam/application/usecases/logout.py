from loguru import logger

from src.core.iam.presentation.dto import RefreshData
from src.core.iam.application.interfaces.uow import IIAMUnitOfWork


class LogoutUserUseCase:
    def __init__(self, unit_of_work: IIAMUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, refresh_data: RefreshData):
        async with self.unit_of_work as uow:
            account = await uow.account.find_by_token_value(refresh_data.refresh_token)
            if not account:
                return

            account.logout(refresh_data.refresh_token)

            await uow.account.save(account)
            await uow.commit()

        logger.info("Logged out user | account_id={}", account.id)
