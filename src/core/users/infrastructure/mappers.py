from typing import Union

from src.core.users.domain.entities import UserAggregate, UserAuthEntity, IndividualUserEntity, BusinessUserEntity, \
    AuthTokenAggregate
from src.core.users.domain.enums import UserRoleEnum
from src.configuration.database.models.users import User, IndividualProfile, BusinessProfile, UserAuth, AuthToken
from src.core.users.domain.value_objects import Fullname, Email, Phone, OrganizationFullname, IIN, BIN, HashedPassword


class UserMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> User:
        user_model = User(
            id=user_aggregate.id,
            role=user_aggregate.role,
            first_name=user_aggregate.fullname.first_name,
            last_name=user_aggregate.fullname.last_name,
            patronymic=user_aggregate.fullname.patronymic,
            email=user_aggregate.email.value,
            phone=user_aggregate.phone.value,
            is_active=user_aggregate.is_active
        )

        profile_model = UserProfileMapper.to_orm(user_aggregate)
        user_model.auth = UserAuthMapper.to_orm(user_aggregate)

        match profile_model:
            case IndividualProfile():
                user_model.individual_profile = profile_model
            case BusinessProfile():
                user_model.business_profile = profile_model
            case _:
                raise ValueError(f"Unsupported profile type: {type(profile_model)}")

        return user_model

    @staticmethod
    def to_domain(user_model: User):
        profile = UserProfileMapper.to_domain(user_model)
        authentication = UserAuthMapper.to_domain(user_model.auth)

        return UserAggregate(
            id=user_model.id,
            role=user_model.role,
            fullname=Fullname.from_raw(
                first_name=user_model.first_name,
                last_name=user_model.last_name,
                patronymic=user_model.patronymic
            ),
            email=Email.from_raw(user_model.email),
            phone=Phone.from_raw(user_model.phone),
            is_active=user_model.is_active,
            profile=profile,
            authentication=authentication
        )


class UserProfileMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> Union[IndividualProfile, BusinessProfile]:
        if user_aggregate.role == UserRoleEnum.INDIVIDUAL:
            return IndividualUserMapper.to_orm(user_aggregate)

        if user_aggregate.role == UserRoleEnum.BUSINESS:
            return BusinessUserMapper.to_orm(user_aggregate)

        raise ValueError("Unsupported profile type ...")

    @staticmethod
    def to_domain(user_model: User) -> Union[IndividualUserEntity, BusinessUserEntity]:
        if user_model.individual_profile:
            return IndividualUserMapper.to_domain(user_model.individual_profile)

        if user_model.business_profile:
            return BusinessUserMapper.to_domain(user_model.business_profile)

        raise ValueError("Unsupported profile type ...")


class IndividualUserMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> IndividualProfile:
        return IndividualProfile(
            id=user_aggregate.profile.id,
            user_id=user_aggregate.id
        )

    @staticmethod
    def to_domain(individual_model: IndividualProfile) -> IndividualUserEntity:
        return IndividualUserEntity(
            id=individual_model.id
        )


class BusinessUserMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> BusinessProfile:
        return BusinessProfile(
            id=user_aggregate.profile.id,
            user_id=user_aggregate.id,
            business_type=user_aggregate.profile.business_type,
            organization_fullname=user_aggregate.profile.organization_fullname.value,
            iin=user_aggregate.profile.iin.value,
            bin=user_aggregate.profile.bin.value
        )

    @staticmethod
    def to_domain(business_model: BusinessProfile) -> BusinessUserEntity:
        return BusinessUserEntity(
            id=business_model.id,
            business_type=business_model.business_type,
            organization_fullname=OrganizationFullname.from_raw(business_model.organization_fullname),
            iin=IIN.from_raw(business_model.iin),
            bin=BIN.from_raw(business_model.bin)
        )


class UserAuthMapper:
    @staticmethod
    def to_orm(user_aggregate: UserAggregate) -> UserAuth:
        return UserAuth(
            id=user_aggregate.authentication.id,
            user_id=user_aggregate.id,
            hashed_password=user_aggregate.authentication.password.hashed_password
        )

    @staticmethod
    def to_domain(auth_model: UserAuth) -> UserAuthEntity:
        return UserAuthEntity(
            id=auth_model.id,
            password=HashedPassword.from_hash(auth_model.hashed_password)
        )


class AuthTokenMapper:
    @staticmethod
    def to_orm(token_aggregate: AuthTokenAggregate) -> AuthToken:
        return AuthToken(
            id=token_aggregate.id,
            user_id=token_aggregate.user_id,
            token_type=token_aggregate.token_type,
            token_value=token_aggregate.token_value,
            is_revoked=token_aggregate.is_revoked,
            expires_at=token_aggregate.expires_at
        )

    @staticmethod
    def to_domain(token_model: AuthToken) -> AuthTokenAggregate:
        return AuthTokenAggregate(
            id=token_model.id,
            user_id=token_model.user_id,
            token_type=token_model.token_type,
            token_value=token_model.token_value,
            is_revoked=token_model.is_revoked,
            expires_at=token_model.expires_at
        )
