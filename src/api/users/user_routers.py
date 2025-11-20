from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.users.user_dto import (
    FullnameDTO,
    EmailDTO,
    PhoneDTO,
    OrganizationFullnameDTO,
    DocumentValueDTO,
    AvatarUrlDTO,
    ChangePasswordDTO
)

from src.configuration.dependencies.depends import DependencyContainer

from src.core.users.application.usecases import (
    ChangeFullnameUseCase,
    ChangeEmailUseCase,
    ChangePhoneUseCase,
    ChangeOrganizationFullnameUseCase,
    ChangeDocumentValueUseCase,
    ChangeAvatarURLUsecase,
    ChangePasswordUseCase
)


users_router = APIRouter(prefix="/api/v1", tags=["Users"])


@users_router.patch("/users/me/change-fullname")
@inject
async def change_fullname(
    fullname_dto: FullnameDTO,
    change_fullname_usecase: Annotated[
        ChangeFullnameUseCase,
        Depends(
            Provide[
                DependencyContainer.change_fullname_usecase
            ]
        )
    ]
):
    await change_fullname_usecase.execute(fullname_dto)
    return {"message": "Данные успешно изменены"}


@users_router.patch("/users/me/change-email")
@inject
async def change_email(
    email_dto: EmailDTO,
    change_email_usecase: Annotated[
        ChangeEmailUseCase,
        Depends(
            Provide[
                DependencyContainer.change_email_usecase
            ]
        )
    ]
):
    await change_email_usecase.execute(email_dto)
    return {"message": "Email успешно изменен"}


@users_router.patch("/users/me/change-phone")
@inject
async def change_phone(
    phone_dto: PhoneDTO,
    change_phone_usecase: Annotated[
        ChangePhoneUseCase,
        Depends(
            Provide[
                DependencyContainer.change_phone_usecase
            ]
        )
    ]
):
    await change_phone_usecase.execute(phone_dto)
    return {"message": "Номер телефона успешно изменен"}


@users_router.patch("/users/me/change-organization-fullname")
@inject
async def change_organization_fullname(
    organization_fullname_dto: OrganizationFullnameDTO,
    change_organization_fullname_usecase: Annotated[
        ChangeOrganizationFullnameUseCase,
        Depends(
            Provide[
                DependencyContainer.change_organization_fullname_usecase
            ]
        )
    ]
):
    await change_organization_fullname_usecase.execute(organization_fullname_dto)
    return {"message": "Наименование организации успешно изменено"}


@users_router.patch("/users/me/change-document-value")
@inject
async def change_document_value(
    document_value_dto: DocumentValueDTO,
    change_document_value_usecase: Annotated[
        ChangeDocumentValueUseCase,
        Depends(
            Provide[
                DependencyContainer.change_document_value_usecase
            ]
        )
    ]
):
    await change_document_value_usecase.execute(document_value_dto)
    return {"message": "Документ был успешно изменен"}


@users_router.patch("/users/me/change-avatar-url")
@inject
async def change_avatar_url(
    avatar_url_dto: AvatarUrlDTO,
    change_avatar_url_usecase: Annotated[
        ChangeAvatarURLUsecase,
        Depends(
            Provide[
                DependencyContainer.change_avatar_url_usecase
            ]
        )
    ]
):
    await change_avatar_url_usecase.execute(avatar_url_dto)
    return {"message": "Ваш аватар успешно изменен"}


@users_router.patch("/users/me/change-password")
@inject
async def change_password(
    change_password_dto: ChangePasswordDTO,
    change_password_usecase: Annotated[
        ChangePasswordUseCase,
        Depends(
            Provide[
                DependencyContainer.change_password_usecase
            ]
        )
    ]
):
    await change_password_usecase.execute(change_password_dto)
    return {"message": "Пароль успешно изменен"}
