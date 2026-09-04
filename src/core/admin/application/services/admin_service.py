from uuid import UUID

from src.core.admin.application.interfaces.uow import IAdminUnitOfWork
from src.core.admin.domain.exceptions import AdminAlreadyExistsError, AdminNotFoundError
from src.core.admin.presentation.dto import CreateAdminRequest
from src.core.iam.application.interfaces.repository import IAccountRepository
from src.core.iam.domain.exceptions import AccountNotFoundError


class AdminService:
    def __init__(self, uow: IAdminUnitOfWork, account_repository: IAccountRepository):
        self.uow = uow
        self.account_repository = account_repository

    async def create_admin(self, account_id: UUID, dto: CreateAdminRequest) -> None:
        target_account = await self.account_repository.get_account_by_email(
            dto.target_email
        )
        if not target_account:
            raise AccountNotFoundError()

        async with self.uow as uow:
            initiator = await uow.admin.get_by_account_id(account_id)
            if not initiator:
                raise AdminNotFoundError()

            existing = await uow.admin.get_by_account_id(target_account.id)
            if existing:
                raise AdminAlreadyExistsError()

            admin = initiator.add_admin(
                account_id=target_account.id,
                last_name=dto.last_name,
                first_name=dto.first_name,
                patronymic=dto.patronymic,
                role=dto.role,
            )

            await uow.admin.save(admin)
            await uow.commit()
