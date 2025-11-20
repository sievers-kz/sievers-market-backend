import uuid

from src.api.users.user_dto import PhoneDTO
from src.core.auth.domain.enums import TokenTypeEnum
from src.core.auth.infrastructure.services.pyjwt_token import AbstractTokenService
from src.core.shared.infrastructure.services.phone_normalizer import AbstractPhoneNormalizer
from src.core.users.application.abstract_user_uow import AbstractUserUnitOfWork


class ChangePhoneUseCase:
    def __init__(
        self,
        unit_of_work: AbstractUserUnitOfWork,
        token_service: AbstractTokenService,
        phone_normalizer: AbstractPhoneNormalizer
    ):
        self.unit_of_work = unit_of_work
        self.token_service = token_service
        self.phone_normalizer = phone_normalizer

    async def execute(self, phone_dto: PhoneDTO):
        payload = self.token_service.verify_token(phone_dto.access_token, TokenTypeEnum.ACCESS_TOKEN)
        user_id = uuid.UUID(payload.get("sub"))

        async with self.unit_of_work as uow:
            user = await uow.user.get_user_by_id(user_id)
            normalized_phone = self.phone_normalizer.normalize(phone_dto.phone)
            user.change_phone(normalized_phone)

            await uow.user.save(user)
            await uow.commit()

