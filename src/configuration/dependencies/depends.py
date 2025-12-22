from datetime import timedelta

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.auth.application.usecases import (
    CreateUserUseCase,
    EmailConfirmationUseCase,
    LoginUserUseCase,
    RefreshTokenUseCase,
    LogoutUserUseCase,
    ForgotPasswordUseCase,
    ResetPasswordUseCase
)
from src.core.listings.application.usecases import GetListingCreationSchemaUseCase, CreateListingUseCase, \
    UpdateListingSchemaUseCase, UpdateListingUseCase, GetUserListingsUseCase, CreateDraftListingUseCase, \
    ActivateListingUseCase, DeactivateListingUseCase, ArchiveListingUseCase, DeleteListingUseCase, \
    GetPublicListingsUseCase, GetDetailPublicListingUseCase, SearchListingsUseCase
from src.core.listings.infrastructure.filter_builder import FilterBuilderService
from src.core.listings.infrastructure.form_builder import ListingFormBuilderService
from src.core.listings.infrastructure.listing_unit_of_work import ListingUnitOfWork
from src.core.listings.infrastructure.query_services.listing_query_context import ListingQueryContext
from src.core.references.application.usecases.categories_tree import GetCategoriesTreeUseCase
from src.core.references.infrastructure.queries.reference_query_context import ReferenceQueryContext

from src.core.shared.infrastructure.services.phone_normalizer import PhoneNormalizer

from src.core.users.application.usecases import (
    ChangeFullnameUseCase,
    ChangeEmailUseCase,
    ChangePhoneUseCase,
    ChangeOrganizationFullnameUseCase,
    ChangeDocumentValueUseCase,
    ChangeAvatarURLUsecase,
    ChangePasswordUseCase
)

from src.core.auth.infrastructure.auth_unit_of_work import AuthUnitOfWork

from src.core.shared.infrastructure.services.email_sender import ConsoleEmailSender, SendGridEmailSender
from src.core.shared.infrastructure.services.password_hasher import BcryptPasswordHasher
from src.core.auth.infrastructure.services.pyjwt_token import PyJWTTokenService
from src.core.shared.infrastructure.composite_uow import UserIdentityUnitOfWork
from src.core.users.infrastructure.user_unit_of_work import UserUnitOfWork


class DependencyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.users.user_routers",
            "src.api.auth.auth_routers",
            "src.api.references.routers",
            "src.api.shared.security",
            "src.api.listings.routers"
        ]
    )

    config = providers.Configuration()

    async_engine = providers.Singleton(
        create_async_engine,
        url=config.database_url,
        echo=True
    )

    async_session_maker = providers.Singleton(
        sessionmaker,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

    user_unit_of_work = providers.Factory(
        UserUnitOfWork,
        session_factory=async_session_maker
    )
    identity_unit_of_work = providers.Factory(
        AuthUnitOfWork,
        session_factory=async_session_maker
    )

    listing_unit_of_work = providers.Factory(
        ListingUnitOfWork,
        session_factory=async_session_maker
    )

    user_identity_unit_of_work = providers.Factory(
        UserIdentityUnitOfWork,
        session_factory=async_session_maker
    )

    reference_query_context = providers.Factory(
        ReferenceQueryContext,
        session_factory=async_session_maker
    )

    listing_query_context = providers.Factory(
        ListingQueryContext,
        session_factory=async_session_maker
    )

    password_hasher = providers.Singleton(BcryptPasswordHasher)
    phone_normalizer = providers.Singleton(PhoneNormalizer)
    console_email_sender = providers.Singleton(ConsoleEmailSender)
    form_builder = providers.Factory(ListingFormBuilderService)
    filter_builder = providers.Factory(FilterBuilderService)

    sendgrid_email_sender = providers.Singleton(
        SendGridEmailSender,
        api_key=config.SEND_GRID_API_KEY,
        from_email=config.FROM_EMAIL,
        email_confirmation_template_id=config.EMAIL_CONFIRMATION_TEMPLATE_ID,
        password_reset_template_id=config.PASSWORD_RESET_TEMPLATE_ID
    )

    token_service = providers.Singleton(
        PyJWTTokenService,
        secret_key=config.SECRET_KEY,
        algorithm=config.ALGORITHM,

        access_token_lifetime=providers.Factory(
            timedelta,
            minutes=config.ACCESS_TOKEN_LIFETIME.as_int()
        ),
        refresh_token_lifetime=providers.Factory(
            timedelta,
            days=config.REFRESH_TOKEN_LIFETIME.as_int()
        ),
        email_token_lifetime=providers.Factory(
            timedelta,
            hours=config.EMAIL_TOKEN_LIFETIME.as_int()
        ),
        password_reset_token_lifetime=providers.Factory(
            timedelta,
            hours=config.PASSWORD_RESET_TOKEN_LIFETIME.as_int()
        )
    )

    create_user_usecase = providers.Factory(
        CreateUserUseCase,
        unit_of_work=user_identity_unit_of_work,
        email_sender=console_email_sender,
        token_service=token_service
    )

    email_confirmation_usecase = providers.Factory(
        EmailConfirmationUseCase,
        unit_of_work=user_identity_unit_of_work
    )

    login_user_usecase = providers.Factory(
        LoginUserUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=token_service,
        password_hasher=password_hasher
    )

    refresh_token_usecase = providers.Factory(
        RefreshTokenUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=token_service
    )

    logout_user_usecase = providers.Factory(
        LogoutUserUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=token_service
    )

    forgot_password_usecase = providers.Factory(
        ForgotPasswordUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=token_service,
        email_sender=console_email_sender
    )

    reset_password_usecase = providers.Factory(
        ResetPasswordUseCase,
        unit_of_work=user_identity_unit_of_work,
        token_service=token_service,
        password_hasher=password_hasher
    )

    change_fullname_usecase = providers.Factory(
        ChangeFullnameUseCase,
        unit_of_work=user_unit_of_work,
        token_service=token_service
    )

    change_email_usecase = providers.Factory(
        ChangeEmailUseCase,
        unit_of_work=user_unit_of_work,
        token_service=token_service
    )

    change_phone_usecase = providers.Factory(
        ChangePhoneUseCase,
        unit_of_work=user_unit_of_work,
        token_service=token_service,
        phone_normalizer=phone_normalizer
    )

    change_organization_fullname_usecase = providers.Factory(
        ChangeOrganizationFullnameUseCase,
        unit_of_work=user_unit_of_work,
        token_service=token_service,
    )

    change_document_value_usecase = providers.Factory(
        ChangeDocumentValueUseCase,
        unit_of_work=user_unit_of_work,
        token_service=token_service,
    )

    change_avatar_url_usecase = providers.Factory(
        ChangeAvatarURLUsecase,
        unit_of_work=user_unit_of_work,
        token_service=token_service
    )

    change_password_usecase = providers.Factory(
        ChangePasswordUseCase,
        unit_of_work=identity_unit_of_work,
        token_service=token_service,
        password_hasher=password_hasher
    )

    get_categories_tree_usecase = providers.Factory(
        GetCategoriesTreeUseCase,
        query_service=reference_query_context
    )

    listing_creation_schema_usecase = providers.Factory(
        GetListingCreationSchemaUseCase,
        query_service=reference_query_context,
        form_builder=form_builder
    )

    create_listing_usecase = providers.Factory(
        CreateListingUseCase,
        unit_of_work=listing_unit_of_work,
        query_service=reference_query_context
    )

    update_listing_schema_usecase = providers.Factory(
        UpdateListingSchemaUseCase,
        listing_query_service=listing_query_context,
        reference_query_service=reference_query_context,
        form_builder=form_builder
    )

    update_listing_usecase = providers.Factory(
        UpdateListingUseCase,
        unit_of_work=listing_unit_of_work,
    )

    get_user_listings_usecase = providers.Factory(
        GetUserListingsUseCase,
        query_service=listing_query_context
    )

    create_draft_listing_usecase = providers.Factory(
        CreateDraftListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    activate_listing_usecase = providers.Factory(
        ActivateListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    deactivate_listing_usecase = providers.Factory(
        DeactivateListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    archive_listing_usecase = providers.Factory(
        ArchiveListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    delete_listing_usecase = providers.Factory(
        DeleteListingUseCase,
        unit_of_work=listing_unit_of_work
    )

    get_public_listings_usecase = providers.Factory(
        GetPublicListingsUseCase,
        filter_builder=filter_builder,
        query_service=listing_query_context
    )

    get_detail_public_listing_usecase = providers.Factory(
        GetDetailPublicListingUseCase,
        query_service=listing_query_context
    )

    search_listings_usecase = providers.Factory(
        SearchListingsUseCase,
        query_service=listing_query_context
    )
