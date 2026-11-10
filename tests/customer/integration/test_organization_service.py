import uuid

import pytest

from src.core.customer.domain.enums import RegistryStatus
from src.core.customer.domain.exceptions import OrganizationCannotPublishError, OrganizationNotFoundError
from tests.customer.conftest import create_domain_organization


class TestOrganizationServiceEnsureCanPublish:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_passes_for_own_verified_organization(self, organization_service, create_organization):
        await organization_service.ensure_can_publish(create_organization.owner_id, create_organization.id)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_organization_raises_not_found(self, organization_service, create_customer):
        with pytest.raises(OrganizationNotFoundError):
            await organization_service.ensure_can_publish(create_customer.id, uuid.uuid4())

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_organization_raises_not_found(
        self, organization_service, create_organization, other_customer
    ):
        with pytest.raises(OrganizationNotFoundError):
            await organization_service.ensure_can_publish(other_customer.id, create_organization.id)

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("status", [RegistryStatus.PENDING, RegistryStatus.NOT_FOUND])
    async def test_unverified_organization_cannot_publish(
        self, status, organization_service, create_customer, save_organization
    ):
        organization = await save_organization(
            create_domain_organization(owner_id=create_customer.id, registry_status=status)
        )

        with pytest.raises(OrganizationCannotPublishError):
            await organization_service.ensure_can_publish(create_customer.id, organization.id)


class TestOrganizationServiceIsOwner:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_owner(self, organization_service, create_organization):
        assert await organization_service.is_owner(create_organization.owner_id, create_organization.id) is True

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_not_owner(self, organization_service, create_organization, other_customer):
        assert await organization_service.is_owner(other_customer.id, create_organization.id) is False

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_organization(self, organization_service, create_customer):
        assert await organization_service.is_owner(create_customer.id, uuid.uuid4()) is False

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_ignores_registry_status(self, organization_service, create_customer, save_organization):
        organization = await save_organization(
            create_domain_organization(owner_id=create_customer.id, registry_status=RegistryStatus.NOT_FOUND)
        )

        assert await organization_service.is_owner(create_customer.id, organization.id) is True
