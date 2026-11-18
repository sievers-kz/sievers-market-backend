import pytest


class TestListingSearchSync:
    """Use case'ы после коммита синхронизируют индекс (Meilisearch подменён моком в `tests/conftest.py`)."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_indexes_only_filterable_attributes(
        self,
        container,
        create_listing_usecase,
        create_organization,
        create_listing_request,
        mock_search_service,
    ):
        dto = create_listing_request
        await create_listing_usecase.execute(create_organization.owner_id, dto)

        filterable_keys = await container.catalog.catalog_service().get_filterable_keys(dto.subcategory_id)
        document = mock_search_service.index_documents.await_args.kwargs["documents"][0]

        for key in dto.attributes:
            assert (key in document) == (key in filterable_keys)
        assert document["created_at"] is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_deactivate_removes_from_index(
        self,
        create_listing_usecase,
        deactivate_listing_usecase,
        create_organization,
        create_listing_request,
        mock_search_service,
    ):
        listing_id = await create_listing_usecase.execute(create_organization.owner_id, create_listing_request)

        await deactivate_listing_usecase.execute(create_organization.owner_id, listing_id)

        mock_search_service.delete_documents.assert_awaited_once_with(
            index_name="listing",
            document_ids=[str(listing_id)],
        )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_activate_returns_to_index(
        self,
        create_listing_usecase,
        deactivate_listing_usecase,
        activate_listing_usecase,
        create_organization,
        create_listing_request,
        mock_search_service,
    ):
        listing_id = await create_listing_usecase.execute(create_organization.owner_id, create_listing_request)
        await deactivate_listing_usecase.execute(create_organization.owner_id, listing_id)
        mock_search_service.index_documents.reset_mock()

        await activate_listing_usecase.execute(create_organization.owner_id, listing_id)

        document = mock_search_service.index_documents.await_args.kwargs["documents"][0]
        assert document["id"] == str(listing_id)
        assert document["is_active"] is True
