import pytest

from src.core.customer.domain.enums import RegistryStatus
from src.core.customer.domain.exceptions import OrganizationCannotPublishError, OrganizationNotFoundError
from src.core.listing.domain.exceptions import ListingNotFoundError
from src.core.listing.presentation.dto import ChangeListingPriceRequest
from src.core.shared.domain.enums import PriceCurrency
from tests.customer.conftest import create_domain_organization


class TestCreateListingOrganizationAccess:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_listing_belongs_to_selected_organization(
        self, create_listing_usecase, create_organization, create_listing_request, listing_repository
    ):
        listing_id = await create_listing_usecase.execute(create_organization.owner_id, create_listing_request)

        listing = await listing_repository.get_by_id(listing_id)
        assert listing.organization_id == create_organization.id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_customer_with_several_organizations_picks_one(
        self, create_listing_usecase, create_organization, save_organization, create_listing_request, listing_repository
    ):
        second = await save_organization(
            create_domain_organization(owner_id=create_organization.owner_id, registry_status=RegistryStatus.VERIFIED)
        )
        dto = create_listing_request.model_copy(update={"organization_id": second.id})

        listing_id = await create_listing_usecase.execute(create_organization.owner_id, dto)

        assert (await listing_repository.get_by_id(listing_id)).organization_id == second.id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_unverified_organization_cannot_create(
        self, create_listing_usecase, create_customer, save_organization, create_listing_request
    ):
        pending = await save_organization(create_domain_organization(owner_id=create_customer.id))
        dto = create_listing_request.model_copy(update={"organization_id": pending.id})

        with pytest.raises(OrganizationCannotPublishError):
            await create_listing_usecase.execute(create_customer.id, dto)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_organization_cannot_create(
        self, create_listing_usecase, other_customer, create_listing_request
    ):
        with pytest.raises(OrganizationNotFoundError):
            await create_listing_usecase.execute(other_customer.id, create_listing_request)


class TestChangeListingOrganizationAccess:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_foreign_customer_cannot_change_listing(
        self, create_listing, change_listing_price_usecase, other_customer, listing_repository
    ):
        dto = ChangeListingPriceRequest(price="100", currency=PriceCurrency.USD)

        with pytest.raises(ListingNotFoundError):
            await change_listing_price_usecase.execute(other_customer.id, create_listing.id, dto)

        assert (await listing_repository.get_by_id(create_listing.id)).price == create_listing.price

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_owner_can_change_listing(
        self, create_listing, change_listing_price_usecase, create_organization, listing_repository
    ):
        dto = ChangeListingPriceRequest(price="100", currency=PriceCurrency.USD)

        await change_listing_price_usecase.execute(create_organization.owner_id, create_listing.id, dto)

        assert (await listing_repository.get_by_id(create_listing.id)).price == 100
