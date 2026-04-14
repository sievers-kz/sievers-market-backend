from src.core.customer.application.interfaces.abstract_customer_service import ICustomerService
from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.enums import OTPType
from src.core.iam.presentation.dto import CreateUserRequest
from src.core.iam.application.interfaces.abstract_factory import IAccountFactory
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork


class CreateUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        factory: IAccountFactory,
        customer_service: ICustomerService,
        otp_service: OTPService,
    ):
        self.unit_of_work = unit_of_work
        self.factory = factory
        self.customer_service = customer_service
        self.otp_service = otp_service

    async def execute(self, dto: CreateUserRequest):
        async with self.unit_of_work as uow:
            existing = await uow.account.get_account_by_email(dto.email)
            if existing:
                raise ValueError("Пользователь с таким email уже существует")

            account = self.factory.create(dto)
            await uow.account.save(account)

            await self.customer_service.create(account_id=account.id, last_name=dto.last_name, first_name=dto.first_name)
            await uow.commit()

        await self.otp_service.send(
            account_id=account.id,
            email=dto.email,
            otp_type=OTPType.CONFIRMATION,
        )

        return account.id
