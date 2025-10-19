import uuid

from src.api.users.user_dto import UserDTO, IndividualUserDTO, BusinessUserDTO, UserAuthDTO
from src.core.users.domain.entities import IndividualUserEntity, BusinessUserEntity, UserAggregate, UserAuthEntity
from src.core.users.domain.enums import UserRoleEnum
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
            is_active=False,
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
        return IndividualUserEntity(id=uuid.uuid4())


class BusinessUserFactory:
    @staticmethod
    def create(business_dto: BusinessUserDTO):
        return BusinessUserEntity(
            id=uuid.uuid4(),
            business_type=business_dto.business_type,
            organization_fullname=OrganizationFullname.from_raw(business_dto.organization_fullname),
            iin=IIN.from_raw(business_dto.iin),
            bin=BIN.from_raw(business_dto.bin)
        )


class UserAuthFactory:
    @staticmethod
    def create(auth_dto: UserAuthDTO):
        return UserAuthEntity(
            id=uuid.uuid4(),
            password=HashedPassword.from_raw(auth_dto.password)
        )

