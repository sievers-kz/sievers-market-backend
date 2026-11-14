import uuid

import pytest

from src.core.customer.domain.exceptions import InvalidShopNameError, OrganizationNotFoundError
from src.core.customer.presentation.dto import (
    ChangeOrganizationContactEmailRequest,
    ChangeOrganizationContactPhoneRequest,
    ChangeOrganizationShopNameRequest,
)
from src.core.shared.domain.exceptions import InvalidPhoneFormatError
from tests.customer.conftest import create_domain_organization


class TestChangeOrganizationShopNameUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_owner_changes_shop_name(
        self, change_organization_shop_name_usecase, create_customer, save_organization, get_organization
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        await change_organization_shop_name_usecase.execute(
            create_customer.id, organization.id, ChangeOrganizationShopNameRequest(shop_name="  Olzha   Agro ")
        )

        assert (await get_organization(organization.id)).shop_name == "Olzha Agro"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_invalid_shop_name_is_rejected_and_not_saved(
        self, change_organization_shop_name_usecase, create_customer, save_organization, get_organization
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        with pytest.raises(InvalidShopNameError):
            await change_organization_shop_name_usecase.execute(
                create_customer.id, organization.id, ChangeOrganizationShopNameRequest(shop_name="A")
            )

        assert (await get_organization(organization.id)).shop_name is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_organization_raises_not_found_and_is_kept(
        self,
        change_organization_shop_name_usecase,
        create_customer,
        other_customer,
        save_organization,
        get_organization,
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        with pytest.raises(OrganizationNotFoundError):
            await change_organization_shop_name_usecase.execute(
                other_customer.id, organization.id, ChangeOrganizationShopNameRequest(shop_name="Olzha Agro")
            )

        assert (await get_organization(organization.id)).shop_name is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_organization_raises_not_found(self, change_organization_shop_name_usecase, create_customer):
        with pytest.raises(OrganizationNotFoundError):
            await change_organization_shop_name_usecase.execute(
                create_customer.id, uuid.uuid4(), ChangeOrganizationShopNameRequest(shop_name="Olzha Agro")
            )


class TestChangeOrganizationContactPhoneUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("raw_phone", ["+7 701 123 45 67", "8 (701) 123-45-67", "+77011234567"])
    async def test_owner_changes_phone_and_it_is_normalized(
        self, raw_phone, change_organization_contact_phone_usecase, create_customer, save_organization, get_organization
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        await change_organization_contact_phone_usecase.execute(
            create_customer.id, organization.id, ChangeOrganizationContactPhoneRequest(contact_phone=raw_phone)
        )

        assert (await get_organization(organization.id)).contact_phone == "+77011234567"

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("raw_phone", ["abc", "", "123", "+1 202 555 0100"])
    async def test_invalid_phone_is_rejected_and_not_saved(
        self, raw_phone, change_organization_contact_phone_usecase, create_customer, save_organization, get_organization
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        with pytest.raises(InvalidPhoneFormatError):
            await change_organization_contact_phone_usecase.execute(
                create_customer.id, organization.id, ChangeOrganizationContactPhoneRequest(contact_phone=raw_phone)
            )

        assert (await get_organization(organization.id)).contact_phone is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_organization_raises_not_found(
        self,
        change_organization_contact_phone_usecase,
        create_customer,
        other_customer,
        save_organization,
        get_organization,
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        with pytest.raises(OrganizationNotFoundError):
            await change_organization_contact_phone_usecase.execute(
                other_customer.id, organization.id, ChangeOrganizationContactPhoneRequest(contact_phone="+77011234567")
            )

        assert (await get_organization(organization.id)).contact_phone is None


class TestChangeOrganizationContactEmailUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_owner_changes_email(
        self, change_organization_contact_email_usecase, create_customer, save_organization, get_organization
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        await change_organization_contact_email_usecase.execute(
            create_customer.id,
            organization.id,
            ChangeOrganizationContactEmailRequest(contact_email="shop@example.com"),
        )

        assert (await get_organization(organization.id)).contact_email == "shop@example.com"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_organization_raises_not_found(
        self,
        change_organization_contact_email_usecase,
        create_customer,
        other_customer,
        save_organization,
        get_organization,
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        with pytest.raises(OrganizationNotFoundError):
            await change_organization_contact_email_usecase.execute(
                other_customer.id,
                organization.id,
                ChangeOrganizationContactEmailRequest(contact_email="shop@example.com"),
            )

        assert (await get_organization(organization.id)).contact_email is None

    @pytest.mark.unit
    @pytest.mark.parametrize("email", ["", "not-an-email", "a@", "@b.com"])
    def test_dto_rejects_malformed_email(self, email):
        with pytest.raises(ValueError):
            ChangeOrganizationContactEmailRequest(contact_email=email)
