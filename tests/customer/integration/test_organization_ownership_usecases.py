import uuid

import pytest

from src.core.customer.domain.enums import RegistryStatus
from src.core.customer.domain.exceptions import OrganizationNotFoundError, OwnershipRequiresRegistryVerificationError
from tests.customer.conftest import create_domain_organization


class TestConfirmOrganizationOwnershipUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_confirms_verified_organization(
        self, confirm_organization_ownership_usecase, create_organization, get_organization
    ):
        await confirm_organization_ownership_usecase.execute(create_organization.id)

        assert (await get_organization(create_organization.id)).is_ownership_verified is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("status", [RegistryStatus.PENDING, RegistryStatus.NOT_FOUND])
    async def test_rejects_organization_not_in_registry(
        self, status, confirm_organization_ownership_usecase, create_customer, save_organization, get_organization
    ):
        organization = await save_organization(
            create_domain_organization(owner_id=create_customer.id, registry_status=status)
        )

        with pytest.raises(OwnershipRequiresRegistryVerificationError):
            await confirm_organization_ownership_usecase.execute(organization.id)

        assert (await get_organization(organization.id)).is_ownership_verified is False

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_organization_raises_not_found(self, confirm_organization_ownership_usecase):
        with pytest.raises(OrganizationNotFoundError):
            await confirm_organization_ownership_usecase.execute(uuid.uuid4())


class TestRevokeOrganizationOwnershipUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_revokes_confirmed_ownership(
        self,
        confirm_organization_ownership_usecase,
        revoke_organization_ownership_usecase,
        create_organization,
        get_organization,
    ):
        await confirm_organization_ownership_usecase.execute(create_organization.id)

        await revoke_organization_ownership_usecase.execute(create_organization.id)

        assert (await get_organization(create_organization.id)).is_ownership_verified is False

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_organization_raises_not_found(self, revoke_organization_ownership_usecase):
        with pytest.raises(OrganizationNotFoundError):
            await revoke_organization_ownership_usecase.execute(uuid.uuid4())
