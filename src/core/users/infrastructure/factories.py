import uuid

from src.api.users.user_dto import UserDTO, IndividualUserDTO, BusinessUserDTO, UserAuthDTO
from src.core.users.domain.entities import IndividualUserEntity, BusinessUserEntity, UserAggregate, UserAuthEntity
from src.core.users.domain.enums import UserRoleEnum
from src.core.users.domain.value_objects import Fullname, Email, Phone, OrganizationFullname, IIN, BIN, Password


class UserFactory:
    @staticmethod
    def create(user_dto: UserDTO):
        profile = UserFactory._create_profile(user_dto.role, user_dto.profile)
        authentication = UserAuthFactory.create(user_dto.authentication)

        return UserAggregate(
            id=uuid.uuid4(),
            role=user_dto.role,
            fullname=Fullname.from_dict(user_dto.dict()),
            email=Email(user_dto.email),
            phone=Phone.from_raw(user_dto.phone),
            profile=profile,
            authentication=authentication
        )

    @staticmethod
    def _create_profile(role: UserRoleEnum, profile_dto):
        match role:
            case UserRoleEnum.INDIVIDUAL:
                return IndividualUserFactory.create(profile_dto)
            case UserRoleEnum.BUSINESS:
                return BusinessUserFactory.create(profile_dto)
            case _:
                raise ValueError(f"Unsupported aggregate role: {role}")


class IndividualUserFactory:
    @staticmethod
    def create(individual_dto: IndividualUserDTO):
        return IndividualUserEntity()


class BusinessUserFactory:
    @staticmethod
    def create(business_dto: BusinessUserDTO):
        return BusinessUserEntity(
            business_type=business_dto.business_type,
            organization_fullname=OrganizationFullname(business_dto.organization_fullname),
            iin=IIN(business_dto.iin),
            bin=BIN(business_dto.bin)
        )


class UserAuthFactory:
    @staticmethod
    def create(auth_dto: UserAuthDTO):
        return UserAuthEntity(
            password=Password.from_raw(auth_dto.password)
        )