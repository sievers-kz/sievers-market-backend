import uuid

import pytest

from src.core.machinery.presentation.filters import MachineryFilter
from src.core.shared.domain.enums import ListingStatus
from tests.machinery.conftest import create_domain_machinery


class TestGetMachineryList:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_machinery_list(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
        default_filter,
    ):
        machinery = None
        for i in range(7):
            machinery = create_domain_machinery(
                customer_id=create_customer.id,
                subcategory_id=ref_ids["subcategory_id"],
                city_id=ref_ids["city_id"],
                brand_id=ref_ids["brand_id"],
                color_id=ref_ids["color_id"],
            )
            await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_list(
            filters=default_filter,
            page=1,
            limit=10,
        )
        ids = [item.id for item in result.items]

        assert machinery.id in ids
        assert result.total == 7
        assert len(result.items) == 7

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_excludes_inactive_machinery(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
        default_filter,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
            color_id=ref_ids["color_id"],
            status=ListingStatus.INACTIVE
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_list(
            filters=default_filter,
            page=1,
            limit=10,
        )

        ids = [item.id for item in result.items]
        assert machinery.id not in ids

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_pagination_structure(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
        default_filter,
    ):
        for i in range(7):
            machinery = create_domain_machinery(
                customer_id=create_customer.id,
                subcategory_id=ref_ids["subcategory_id"],
                city_id=ref_ids["city_id"],
                brand_id=ref_ids["brand_id"],
                color_id=ref_ids["color_id"],
            )
            await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_list(
            filters=default_filter,
            page=1,
            limit=10,
        )

        assert result.total > 1
        assert result.pages_count >= 1
        assert len(result.items) == 7

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_card_fields_populated(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
        default_filter,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
            color_id=ref_ids["color_id"],
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_list(
            filters=default_filter,
            page=1,
            limit=10,
        )
        card = next(i for i in result.items if i.id == machinery.id)

        assert card.title is not None
        assert card.price > 0
        assert card.city is not None
        assert card.subcategory is not None


class TestGetMachineryDetail:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_machinery_detail(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
            color_id=ref_ids["color_id"],
            country_id=ref_ids["country_id"],
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_detail(machinery.id)
        assert result.id == machinery.id
        assert result is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_detail_fields_populated(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
            color_id=ref_ids["color_id"],
            country_id=ref_ids["country_id"],
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_detail(machinery.id)

        assert result.brand is not None
        assert result.subcategory is not None
        assert result.city is not None
        assert result.country is not None
        assert result.color is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_nullable_optional_fields(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_detail(machinery.id)
        assert result.brand is not None
        assert result.color is None
        assert result.country is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_customer_owner_machinery(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_detail(machinery.id)
        assert result.customer is not None
        assert result.customer.id == create_customer.id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_none_for_inactive(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
            status=ListingStatus.INACTIVE,
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_machinery_detail(machinery.id)
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_none_for_nonexistent(self, machinery_query_service):
        result = await machinery_query_service.get_machinery_detail(uuid.uuid4())
        assert result is None


class TestGetCustomerMachinery:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_returns_own_machinery(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
        default_owner_filter,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_customer_machinery(
            customer_id=create_customer.id,
            filters=default_owner_filter,
            page=1,
            limit=10,
        )

        ids = [item.id for item in result.items]
        assert machinery.id in ids

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_does_not_return_other_customer_machinery(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
        default_owner_filter,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_customer_machinery(
            customer_id=uuid.uuid4(),
            filters=default_owner_filter,
            page=1,
            limit=10,
        )

        ids = [item.id for item in result.items]
        assert machinery.id not in ids

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_includes_inactive_for_owner(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
        default_owner_filter,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
            status=ListingStatus.INACTIVE,
        )
        await machinery_repository.save(machinery)

        result = await machinery_query_service.get_customer_machinery(
            customer_id=create_customer.id,
            filters=default_owner_filter,
            page=1,
            limit=10,
        )

        ids = [item.id for item in result.items]
        assert machinery.id in ids


class TestGetMachineryByFilter:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_machinery_list_by_filtered_city(
        self,
        machinery_query_service,
        machinery_repository,
        create_customer,
        ref_ids,
    ):
        machinery = create_domain_machinery(
            customer_id=create_customer.id,
            subcategory_id=ref_ids["subcategory_id"],
            city_id=ref_ids["city_id"],
            brand_id=ref_ids["brand_id"],
        )
        await machinery_repository.save(machinery)

        filters = MachineryFilter(city_id=ref_ids["city_id"])
        result = await machinery_query_service.get_machinery_list(
            filters=filters,
            page=1,
            limit=10,
        )

        ids = [item.id for item in result.items]
        assert machinery.id in ids
        assert all(item.city == "Астана" for item in result.items)