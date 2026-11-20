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


class TestGetSellersCatalog:
    @pytest.fixture
    def save_seller(self, create_customer, save_organization):
        async def _save(
            registry_status=RegistryStatus.VERIFIED, ownership=True, shop_name="Olzha Agro", legal_name=None
        ):
            organization = create_domain_organization(owner_id=create_customer.id, registry_status=registry_status)
            organization.is_ownership_verified = ownership
            organization.shop_name = shop_name
            organization.legal_name = legal_name
            return await save_organization(organization)

        return _save

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_includes_only_registry_verified_with_confirmed_ownership(self, customer_query_service, save_seller):
        shown = await save_seller()
        await save_seller(ownership=False)
        await save_seller(registry_status=RegistryStatus.PENDING, ownership=True)
        await save_seller(registry_status=RegistryStatus.NOT_FOUND, ownership=True)

        result = await customer_query_service.get_sellers_catalog(page=1, limit=20)

        assert [item.id for item in result["items"]] == [shown.id]
        assert result["total"] == 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_name_falls_back_to_legal_name(self, customer_query_service, save_seller):
        await save_seller(shop_name=None, legal_name='ТОО "Тест Агро"')

        result = await customer_query_service.get_sellers_catalog(page=1, limit=20)

        assert result["items"][0].name == 'ТОО "Тест Агро"'

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_does_not_expose_private_fields(self, customer_query_service, save_seller):
        await save_seller()

        result = await customer_query_service.get_sellers_catalog(page=1, limit=20)

        dumped = result["items"][0].model_dump()
        assert not {"tax_id", "contact_phone", "contact_email", "legal_address", "owner_id"} & dumped.keys()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_paginates_without_overlap(self, customer_query_service, save_seller):
        for _ in range(3):
            await save_seller()

        first = await customer_query_service.get_sellers_catalog(page=1, limit=2)
        second = await customer_query_service.get_sellers_catalog(page=2, limit=2)

        ids = [item.id for item in first["items"]] + [item.id for item in second["items"]]
        assert len(ids) == len(set(ids)) == 3
        assert first["total"] == 3
        assert first["pages"] == 2

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_empty_catalog(self, customer_query_service):
        result = await customer_query_service.get_sellers_catalog(page=1, limit=20)

        assert result["items"] == []
        assert result["total"] == 0
