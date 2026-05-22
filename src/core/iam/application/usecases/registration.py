from src.core.customer.application.interfaces.abstract_customer_service import ICustomerService
from src.core.iam.application.interfaces.password_service import IPasswordService
from src.core.iam.application.services.otp import OTPService
from src.core.iam.domain.entities import Account
from src.core.iam.domain.enums import OTPType
from src.core.iam.domain.value_objects import Email, Password
from src.core.iam.presentation.dto import CreateUserRequest
from src.core.iam.application.interfaces.abstract_iam_uow import AbstractIAMUnitOfWork


class CreateUserUseCase:
    def __init__(
        self,
        unit_of_work: AbstractIAMUnitOfWork,
        customer_service: ICustomerService,
        otp_service: OTPService,
        password_service: IPasswordService,
    ):
        self.unit_of_work = unit_of_work
        self.customer_service = customer_service
        self.otp_service = otp_service
        self.password_service = password_service

    async def execute(self, dto: CreateUserRequest):
        async with self.unit_of_work as uow:
            existing = await uow.account.get_account_by_email(dto.email)
            if existing:
                raise ValueError("Пользователь с таким email уже существует")

            self.password_service.validate(dto.raw_password)
            hashed = self.password_service.hash(dto.raw_password)

            account = Account.register(email=Email(dto.email), password=Password(hashed))
            await uow.account.save(account)

            await self.customer_service.create(
                account_id=account.id,
                last_name=dto.last_name,
                first_name=dto.first_name
            )

            await uow.commit()

        await self.otp_service.send(
            account_id=account.id,
            email=dto.email,
            otp_type=OTPType.CONFIRMATION,
        )

        return account.id
