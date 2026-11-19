import json
import uuid

import pytest
from sqlalchemy import text

from src.core.customer.domain.enums import RegistryStatus
from src.core.customer.domain.exceptions import OrganizationNotFoundError
from src.core.listing.domain.enums import ListingStatus
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.presentation.dto import MyListingsSort, MyListingsStatus
from tests.customer.conftest import create_domain_organization
from tests.listing.conftest import create_domain_listing


@pytest.fixture
def listing_query_service(container):
    return container.listing.query_service()


class TestListingQueryServiceDetails:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_details_of_active_listing(self, listing_query_service, create_listing):
        result = await listing_query_service.get_listing_details(create_listing.id)

        assert result.id == create_listing.id
        assert result.owner_id == create_listing.organization_id
        assert result.title == create_listing.title
        assert result.price == create_listing.price

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_listing_raises_not_found(self, listing_query_service):
        with pytest.raises(ListingNotFoundError):
            await listing_query_service.get_listing_details(uuid.uuid4())

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_inactive_listing_raises_not_found(self, listing_query_service, listing_repository, create_listing):
        archived = create_domain_listing(
            create_listing.organization_id,
            create_listing.city_id,
            create_listing.category_id,
            create_listing.subcategory_id,
        )
        archived.status = ListingStatus.ARCHIVED
        await listing_repository.save(archived)

        with pytest.raises(ListingNotFoundError):
            await listing_query_service.get_listing_details(archived.id)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_category_and_seller(self, listing_query_service, create_listing, create_organization):
        result = await listing_query_service.get_listing_details(create_listing.id)

        assert result.category_id == create_listing.category_id
        assert result.subcategory_id == create_listing.subcategory_id
        assert result.category
        assert result.seller.organization_id == create_organization.id
        assert result.seller.name == (create_organization.shop_name or create_organization.legal_name)
        assert result.seller.phone == create_organization.contact_phone
        assert result.created_at is not None


class TestListingQueryServiceDetailSpecs:
    """Характеристики на тракторе: в seed-настройке у «Колесные тракторы» есть марка, состояние, мощность."""

    @pytest.fixture
    def tractor_listing(self, listing_repository, create_organization, database_session):
        async def _make(attributes: dict):
            city_id = (await database_session.execute(text("SELECT id FROM cities LIMIT 1"))).scalar_one()
            subcategory_id, category_id = (
                await database_session.execute(
                    text("SELECT id, category_id FROM subcategories WHERE name = 'Колесные тракторы'")
                )
            ).one()
            listing = create_domain_listing(create_organization.id, city_id, category_id, subcategory_id)
            await listing_repository.save(listing)
            await database_session.execute(
                text("UPDATE listings SET attributes = CAST(:attrs AS jsonb) WHERE id = :id"),
                {"attrs": json.dumps(attributes), "id": listing.id},
            )
            return listing

        return _make

    @staticmethod
    def _items(result) -> dict:
        return {item.key: item for group in result.specs for item in group.items}

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_resolves_labels_references_and_units(self, listing_query_service, tractor_listing, database_session):
        brand_id, brand_name = (await database_session.execute(text("SELECT id, name FROM brands LIMIT 1"))).one()
        listing = await tractor_listing({"brand": str(brand_id), "condition": "used", "engine_power": 410})

        result = await listing_query_service.get_listing_details(listing.id)
        items = self._items(result)

        assert items["brand"].value == brand_name
        assert items["brand"].label == "Марка"
        assert items["condition"].value == "Б/У"
        assert items["engine_power"].value == 410
        assert items["engine_power"].unit == "л. с."
        assert result.condition == "used"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_skips_empty_unknown_and_stale_values(self, listing_query_service, tractor_listing):
        listing = await tractor_listing(
            {"condition": "broken", "model": "", "engine_power": None, "removed_key": "x", "brand": str(uuid.uuid4())}
        )

        result = await listing_query_service.get_listing_details(listing.id)

        assert self._items(result) == {}
        assert result.specs == []

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_groups_follow_form_order(self, listing_query_service, tractor_listing, database_session):
        brand_id = (await database_session.execute(text("SELECT id FROM brands LIMIT 1"))).scalar_one()
        listing = await tractor_listing({"engine_power": 410, "condition": "new", "brand": str(brand_id)})

        result = await listing_query_service.get_listing_details(listing.id)

        general = result.specs[0]
        assert general.key == "general"
        assert [item.key for item in general.items] == ["brand", "condition"]


class TestListingQueryServiceMyListings:
    @pytest.fixture
    def make_listing(self, listing_repository, database_session):
        """Saves a listing of the given organization. Category and subcategory come from the seeds."""

        async def _make(organization_id, status=ListingStatus.ACTIVE, subcategory_index=0, gallery=True, city=True):
            city_id = (await database_session.execute(text("SELECT id FROM cities LIMIT 1"))).scalar_one()
            subcategory_id, category_id = (
                await database_session.execute(
                    text("SELECT id, category_id FROM subcategories ORDER BY created_at OFFSET :n LIMIT 1"),
                    {"n": subcategory_index},
                )
            ).one()
            listing = create_domain_listing(organization_id, city_id, category_id, subcategory_id)
            listing.status = status
            await listing_repository.save(listing)
            if not gallery:
                await database_session.execute(
                    text("UPDATE listings SET gallery = '[]'::jsonb WHERE id = :id"), {"id": listing.id}
                )
            if not city:
                await database_session.execute(
                    text("UPDATE listings SET city_id = NULL WHERE id = :id"), {"id": listing.id}
                )
            return listing

        return _make

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_only_own_listings(
        self, listing_query_service, make_listing, create_organization, save_organization, other_customer
    ):
        own = await make_listing(create_organization.id)
        foreign_org = await save_organization(
            create_domain_organization(owner_id=other_customer.id, registry_status=RegistryStatus.VERIFIED)
        )
        await make_listing(foreign_org.id)

        result = await listing_query_service.get_my_listings(create_organization.owner_id)

        assert [item.id for item in result["items"]] == [own.id]
        assert result["total"] == 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_card_has_names_and_organization(self, listing_query_service, make_listing, create_organization):
        listing = await make_listing(create_organization.id)

        item = (await listing_query_service.get_my_listings(create_organization.owner_id))["items"][0]

        assert item.id == listing.id
        assert item.organization_id == create_organization.id
        assert item.organization_name == "Olzha Agro"
        assert item.category and item.subcategory and item.city
        assert item.status == ListingStatus.ACTIVE

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_organization_name_falls_back_to_legal_name(
        self, listing_query_service, make_listing, create_customer, save_organization, database_session
    ):
        organization = await save_organization(
            create_domain_organization(owner_id=create_customer.id, registry_status=RegistryStatus.VERIFIED)
        )
        await database_session.execute(
            text("UPDATE organizations SET shop_name = NULL, legal_name = 'ТОО Тест' WHERE id = :id"),
            {"id": organization.id},
        )
        await make_listing(organization.id)

        item = (await listing_query_service.get_my_listings(create_customer.id))["items"][0]

        assert item.organization_name == "ТОО Тест"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_deleted_listings_are_hidden(self, listing_query_service, make_listing, create_organization):
        await make_listing(create_organization.id, status=ListingStatus.DELETED)
        kept = await make_listing(create_organization.id, status=ListingStatus.INACTIVE)

        result = await listing_query_service.get_my_listings(create_organization.owner_id)

        assert [item.id for item in result["items"]] == [kept.id]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filters_by_status(self, listing_query_service, make_listing, create_organization):
        await make_listing(create_organization.id, status=ListingStatus.ACTIVE)
        inactive = await make_listing(create_organization.id, status=ListingStatus.INACTIVE)
        await make_listing(create_organization.id, status=ListingStatus.ARCHIVED)

        result = await listing_query_service.get_my_listings(
            create_organization.owner_id, status=MyListingsStatus.INACTIVE
        )

        assert [item.id for item in result["items"]] == [inactive.id]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_no_status_returns_active_inactive_and_archived(
        self, listing_query_service, make_listing, create_organization
    ):
        for status in (ListingStatus.ACTIVE, ListingStatus.INACTIVE, ListingStatus.ARCHIVED):
            await make_listing(create_organization.id, status=status)

        result = await listing_query_service.get_my_listings(create_organization.owner_id)

        assert result["total"] == 3

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filters_by_organization(
        self, listing_query_service, make_listing, create_organization, save_organization
    ):
        second = await save_organization(
            create_domain_organization(owner_id=create_organization.owner_id, registry_status=RegistryStatus.VERIFIED)
        )
        await make_listing(create_organization.id)
        in_second = await make_listing(second.id)

        result = await listing_query_service.get_my_listings(create_organization.owner_id, organization_id=second.id)

        assert [item.id for item in result["items"]] == [in_second.id]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_organization_raises_not_found(
        self, listing_query_service, create_organization, save_organization, other_customer
    ):
        foreign_org = await save_organization(
            create_domain_organization(owner_id=other_customer.id, registry_status=RegistryStatus.VERIFIED)
        )

        with pytest.raises(OrganizationNotFoundError):
            await listing_query_service.get_my_listings(create_organization.owner_id, organization_id=foreign_org.id)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unknown_organization_raises_not_found(self, listing_query_service, create_organization):
        with pytest.raises(OrganizationNotFoundError):
            await listing_query_service.get_my_listings(create_organization.owner_id, organization_id=uuid.uuid4())

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filters_by_category(
        self, listing_query_service, make_listing, create_organization, database_session
    ):
        first = await make_listing(create_organization.id)
        other_category_id = (
            await database_session.execute(
                text("SELECT category_id FROM subcategories WHERE category_id <> :c LIMIT 1"),
                {"c": first.category_id},
            )
        ).scalar_one_or_none()
        if other_category_id is None:
            pytest.skip("В сидах одна категория")
        second = await make_listing(create_organization.id)
        await database_session.execute(
            text("UPDATE listings SET category_id = :c WHERE id = :id"), {"c": other_category_id, "id": second.id}
        )

        result = await listing_query_service.get_my_listings(
            create_organization.owner_id, category_id=other_category_id
        )

        assert [item.id for item in result["items"]] == [second.id]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_sorts_by_created_at(
        self, listing_query_service, make_listing, create_organization, database_session
    ):
        older = await make_listing(create_organization.id)
        newer = await make_listing(create_organization.id)
        await database_session.execute(
            text("UPDATE listings SET created_at = now() - interval '1 day' WHERE id = :id"), {"id": older.id}
        )

        newest_first = await listing_query_service.get_my_listings(create_organization.owner_id)
        oldest_first = await listing_query_service.get_my_listings(
            create_organization.owner_id, sort=MyListingsSort.OLDEST
        )

        assert [item.id for item in newest_first["items"]] == [newer.id, older.id]
        assert [item.id for item in oldest_first["items"]] == [older.id, newer.id]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_paginates(self, listing_query_service, make_listing, create_organization):
        for _ in range(3):
            await make_listing(create_organization.id)

        page_two = await listing_query_service.get_my_listings(create_organization.owner_id, page=2, limit=2)

        assert page_two["total"] == 3
        assert page_two["pages"] == 2
        assert len(page_two["items"]) == 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_listing_without_photo_and_city(self, listing_query_service, make_listing, create_organization):
        await make_listing(create_organization.id, gallery=False, city=False)

        item = (await listing_query_service.get_my_listings(create_organization.owner_id))["items"][0]

        assert item.preview_image is None
        assert item.city is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_customer_without_listings_gets_empty_page(self, listing_query_service, create_customer):
        result = await listing_query_service.get_my_listings(create_customer.id)

        assert result == {"items": [], "total": 0, "page": 1, "pages": 0}
