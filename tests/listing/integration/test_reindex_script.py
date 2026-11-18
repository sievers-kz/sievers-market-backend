import pytest

from scripts.reindex import reindex


class TestReindexScript:
    """Переиндексация из Postgres; Meilisearch подменён моком в `tests/conftest.py`."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_reindex_clears_and_indexes_only_active(
        self,
        container,
        database_session,
        mock_search_service,
        create_listing_usecase,
        deactivate_listing_usecase,
        create_organization,
        create_listing_request,
    ):
        owner_id = create_organization.owner_id
        active = await create_listing_usecase.execute(owner_id, create_listing_request)
        inactive = await create_listing_usecase.execute(owner_id, create_listing_request)
        await deactivate_listing_usecase.execute(owner_id, inactive)
        mock_search_service.reset_mock()

        service = container.listing.listing_search_service()
        total = await reindex(database_session, service, batch_size=1)

        mock_search_service.configure_index.assert_awaited_once()
        mock_search_service.delete_all_documents.assert_awaited_once_with(index_name="listing")
        indexed_ids = [
            document["id"]
            for call in mock_search_service.index_documents.await_args_list
            for document in call.kwargs["documents"]
        ]
        assert str(active) in indexed_ids
        assert str(inactive) not in indexed_ids
        assert total == len(indexed_ids)
