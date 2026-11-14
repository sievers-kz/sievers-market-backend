import pytest

from src.core.customer.domain.enums import RegistryStatus
from tests.customer.conftest import create_domain_organization


@pytest.fixture
def customer_query_service(container):
    return container.customer.query_service()


class TestGetOrganizationMissingFields:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_lists_unfilled_profile_fields(self, customer_query_service, create_customer, save_organization):
        organization = await save_organization(
            create_domain_organization(
                owner_id=create_customer.id, registry_status=RegistryStatus.VERIFIED, with_profile=False
            )
        )
        organization.change_shop_name("Olzha Agro")
        await save_organization(organization)

        response = await customer_query_service.get_organization(create_customer.id, organization.id)

        assert response.missing_fields == ["contact_phone", "contact_email"]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_empty_for_complete_profile(self, customer_query_service, create_organization):
        response = await customer_query_service.get_organization(create_organization.owner_id, create_organization.id)

        assert response.missing_fields == []
