import uuid
from dataclasses import replace

import pytest

from src.core.customer.domain.entities import Customer
from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.customer.domain.exceptions import OrganizationCannotBeDeletedError, OrganizationNotFoundError
from src.core.customer.presentation.dto import CreateOrganizationRequest
from src.core.iam.domain.value_objects import Email
from tests.customer.conftest import create_domain_organization
from tests.iam.conftest import create_domain_account


class TestDeleteOrganizationUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("status", [RegistryStatus.PENDING, RegistryStatus.NOT_FOUND])
    async def test_deletes_unverified_organization(
        self, status, delete_organization_usecase, create_customer, save_organization, get_organization
    ):
        organization = await save_organization(
            create_domain_organization(owner_id=create_customer.id, registry_status=status)
        )

        await delete_organization_usecase.execute(create_customer.id, organization.id)

        assert await get_organization(organization.id) is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_verified_organization_cannot_be_deleted(
        self, delete_organization_usecase, create_organization, get_organization
    ):
        with pytest.raises(OrganizationCannotBeDeletedError):
            await delete_organization_usecase.execute(create_organization.owner_id, create_organization.id)

        assert await get_organization(create_organization.id) is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_organization_raises_not_found(self, delete_organization_usecase, create_customer):
        with pytest.raises(OrganizationNotFoundError):
            await delete_organization_usecase.execute(create_customer.id, uuid.uuid4())

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_organization_raises_not_found_and_is_kept(
        self,
        delete_organization_usecase,
        create_customer,
        save_organization,
        get_organization,
        account_repository,
        customer_uow,
    ):
        organization = await save_organization(create_domain_organization(owner_id=create_customer.id))

        other_account = replace(create_domain_account(is_active=True), email=Email("other@example.com"))
        await account_repository.save(other_account)
        other_customer = Customer.create(account_id=other_account.id)
        async with customer_uow as uow:
            await uow.customer.save(other_customer)
            await uow.commit()

        with pytest.raises(OrganizationNotFoundError):
            await delete_organization_usecase.execute(other_customer.id, organization.id)

        assert await get_organization(organization.id) is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_tax_id_is_free_again_after_delete(
        self, delete_organization_usecase, create_organization_usecase, create_customer, get_organization
    ):
        dto = CreateOrganizationRequest(kind=Kind.INDIVIDUAL, tax_id="180240041089")
        first = await create_organization_usecase.execute(create_customer.id, dto)

        await delete_organization_usecase.execute(create_customer.id, first.id)
        second = await create_organization_usecase.execute(
            create_customer.id, CreateOrganizationRequest(kind=Kind.COMPANY, tax_id="180240041089")
        )

        assert second.id != first.id
        assert (await get_organization(second.id)).kind == Kind.COMPANY
