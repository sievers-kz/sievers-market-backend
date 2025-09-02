from src.core.users.domain.entities import UserAggregate, UserAuthEntity
from src.core.users.domain.enums import UserRoleEnum
from src.configuration.database.models.users import User, IndividualProfile, BusinessProfile, UserAuth


class UserORMMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> User:
        user_orm = User(
            id=user_aggregate.id,
            role=user_aggregate.role,
            first_name=user_aggregate.fullname.first_name,
            last_name=user_aggregate.fullname.last_name,
            patronymic=user_aggregate.fullname.patronymic,
            email=user_aggregate.email.email,
            phone=user_aggregate.phone.phone,
        )

        profile_orm = UserORMMapper._attach_profile(user_aggregate)
        user_orm.auth = UserAuthMapper.to_orm(user_aggregate)

        match profile_orm:
            case IndividualProfile():
                user_orm.individual_profile = profile_orm
            case BusinessProfile():
                user_orm.business_profile = profile_orm
            case _:
                raise ValueError(f"Unsupported profile type: {type(profile_orm)}")

        return user_orm

    @staticmethod
    def _attach_profile(user_aggregate: UserAggregate):
        match user_aggregate.role:
            case UserRoleEnum.INDIVIDUAL:
                return IndividualUserORMMapper.to_orm(user_aggregate)
            case UserRoleEnum.BUSINESS:
                return BusinessUserORMMapper.to_orm(user_aggregate)
            case _:
                raise ValueError(f"Unsupported role type: {user_aggregate.role}")


class IndividualUserORMMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> IndividualProfile:
        return IndividualProfile(
            user_id=user_aggregate.id
        )


class BusinessUserORMMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> BusinessProfile:
        return BusinessProfile(
            user_id=user_aggregate.id,
            business_type=user_aggregate.profile.business_type,
            organization_fullname=user_aggregate.profile.organization_fullname.organization_fullname,
            iin=user_aggregate.profile.iin.iin,
            bin=user_aggregate.profile.bin.bin
        )


class UserAuthMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> UserAuth:
        return UserAuth(
            user_id=user_aggregate.id,
            hashed_password=user_aggregate.authentication.password.hashed_password
        )