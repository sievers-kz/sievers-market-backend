import uuid
from datetime import datetime

from src.api.users.user_dto import UserDTO, IndividualUserDTO, BusinessUserDTO, UserAuthDTO
from src.core.users.domain.entities import IndividualUserEntity, BusinessUserEntity, UserAggregate, UserAuthEntity, \
    AuthTokenAggregate
from src.core.users.domain.enums import UserRoleEnum, TokenTypeEnum
from src.core.users.domain.value_objects import Fullname, Email, Phone, OrganizationFullname, IIN, BIN, HashedPassword


class UserFactory:
    @staticmethod
    def create(user_dto: UserDTO):
        profile = UserProfileFactory.create(user_dto)
        authentication = UserAuthFactory.create(user_dto.authentication)

        return UserAggregate(
            id=uuid.uuid4(),
            role=user_dto.role,
            fullname=Fullname.from_raw(user_dto.first_name, user_dto.last_name, user_dto.patronymic),
            email=Email.from_raw(user_dto.email),
            phone=Phone.from_raw(user_dto.phone),
            profile=profile,
            authentication=authentication
        )


class UserProfileFactory:
    @staticmethod
    def create(user_dto: UserDTO):
        if user_dto.role == UserRoleEnum.INDIVIDUAL:
            return IndividualUserFactory.create(user_dto.profile)

        if user_dto.role == UserRoleEnum.BUSINESS:
            return BusinessUserFactory.create(user_dto.profile)

        raise ValueError("Unsupported profile type...")


class IndividualUserFactory:
    @staticmethod
    def create(individual_dto: IndividualUserDTO):
        return IndividualUserEntity()


class BusinessUserFactory:
    @staticmethod
    def create(business_dto: BusinessUserDTO):
        return BusinessUserEntity(
            business_type=business_dto.business_type,
            organization_fullname=OrganizationFullname.from_raw(business_dto.organization_fullname),
            iin=IIN.from_raw(business_dto.iin),
            bin=BIN.from_raw(business_dto.bin)
        )


class UserAuthFactory:
    @staticmethod
    def create(auth_dto: UserAuthDTO):
        return UserAuthEntity(
            password=HashedPassword.from_raw(auth_dto.password)
        )


class AuthTokenFactory:
    @staticmethod
    def create_refresh_token(
        user_id: uuid.UUID,
        token_value: str,
        expires_at: datetime
    ):
        return AuthTokenFactory._create(
            user_id=user_id,
            token_type=TokenTypeEnum.REFRESH_TOKEN,
            token_value=token_value,
            expires_at=expires_at
        )

    @staticmethod
    def create_email_token(
        user_id: uuid.UUID,
        token_value: str,
        expires_at: datetime
    ):
        return AuthTokenFactory._create(
            user_id=user_id,
            token_type=TokenTypeEnum.EMAIL_CONFIRMATION_TOKEN,
            token_value=token_value,
            expires_at=expires_at
        )

    @staticmethod
    def _create(
        user_id: uuid.UUID,
        token_type: TokenTypeEnum,
        token_value: str,
        expires_at: datetime
    ):
        return AuthTokenAggregate(
            id=uuid.uuid4(),
            user_id=user_id,
            token_type=token_type,
            token_value=token_value,
            is_revoked=False,
            expires_at=expires_at
        )