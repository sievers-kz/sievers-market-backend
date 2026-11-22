import pytest
from sqlalchemy import text

from src.core.customer.domain.enums import RegistryStatus
from src.core.listing.domain.enums import ListingStatus
from tests.customer.conftest import create_domain_organization
from tests.listing.conftest import create_domain_listing


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


class TestGetOrganizationsCatalog:
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

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20)

        assert [item.id for item in result["items"]] == [shown.id]
        assert result["total"] == 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_name_falls_back_to_legal_name(self, customer_query_service, save_seller):
        await save_seller(shop_name=None, legal_name='ТОО "Тест Агро"')

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20)

        assert result["items"][0].name == 'ТОО "Тест Агро"'

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_does_not_expose_private_fields(self, customer_query_service, save_seller):
        await save_seller()

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20)

        dumped = result["items"][0].model_dump()
        assert set(dumped) == {"id", "name", "logo_media_id", "listings_count"}

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_orders_by_name_ignoring_case(self, customer_query_service, save_seller):
        await save_seller(shop_name="beta")
        await save_seller(shop_name="Gamma")
        await save_seller(shop_name="Alpha")

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20)

        assert [item.name for item in result["items"]] == ["Alpha", "beta", "Gamma"]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_paginates_without_overlap(self, customer_query_service, save_seller):
        for _ in range(3):
            await save_seller()

        first = await customer_query_service.get_organizations_catalog(page=1, limit=2)
        second = await customer_query_service.get_organizations_catalog(page=2, limit=2)

        ids = [item.id for item in first["items"]] + [item.id for item in second["items"]]
        assert len(ids) == len(set(ids)) == 3
        assert first["total"] == 3
        assert first["pages"] == 2

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_empty_catalog(self, customer_query_service):
        result = await customer_query_service.get_organizations_catalog(page=1, limit=20)

        assert result["items"] == []
        assert result["total"] == 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_search_matches_shop_name_and_legal_name_ignoring_case(self, customer_query_service, save_seller):
        by_shop_name = await save_seller(shop_name="Олжа Агро", legal_name='ТОО "Первая"')
        by_legal_name = await save_seller(shop_name="Магазин", legal_name='ТОО "Золотое поле"')
        await save_seller(shop_name="Другой", legal_name='ТОО "Вторая"')

        shop_result = await customer_query_service.get_organizations_catalog(page=1, limit=20, q="олжа")
        legal_result = await customer_query_service.get_organizations_catalog(page=1, limit=20, q="ЗОЛОТОЕ")

        assert [item.id for item in shop_result["items"]] == [by_shop_name.id]
        assert [item.id for item in legal_result["items"]] == [by_legal_name.id]

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("wildcard", ["%", "_"])
    async def test_search_treats_wildcards_as_plain_text(self, wildcard, customer_query_service, save_seller):
        await save_seller(shop_name="Olzha Agro")

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20, q=wildcard)

        assert result["items"] == []

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_search_total_counts_only_matches(self, customer_query_service, save_seller):
        await save_seller(shop_name="Olzha Agro")
        await save_seller(shop_name="Steppe")

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20, q="olzha")

        assert result["total"] == 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_counts_only_active_listings(self, container, customer_query_service, save_seller, database_session):
        organization = await save_seller()
        listing_repository = container.listing.listing_repository()
        city_id = (await database_session.execute(text("SELECT id FROM cities LIMIT 1"))).scalar_one()
        subcategory_id, category_id = (
            await database_session.execute(
                text("SELECT id, category_id FROM subcategories ORDER BY created_at LIMIT 1")
            )
        ).one()
        statuses = (ListingStatus.ACTIVE, ListingStatus.ACTIVE, ListingStatus.INACTIVE, ListingStatus.ARCHIVED)
        for status in statuses:
            listing = create_domain_listing(organization.id, city_id, category_id, subcategory_id)
            listing.status = status
            await listing_repository.save(listing)

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20)

        assert result["items"][0].listings_count == 2

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_organization_without_listings_has_zero_count(self, customer_query_service, save_seller):
        await save_seller()

        result = await customer_query_service.get_organizations_catalog(page=1, limit=20)

        assert result["items"][0].listings_count == 0
