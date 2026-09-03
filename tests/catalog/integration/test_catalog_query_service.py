import pytest
from sqlalchemy import text


class TestCatalogQueryService:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_category_tree_success(self, catalog_query_service):
        result = await catalog_query_service.get_category_tree()

        assert result is not None
        assert len(result) > 0
        assert result[0].name is not None
        assert len(result[0].categories) > 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_subcategory_attributes_success(
        self, catalog_query_service, database_session
    ):
        subcategory_id = (
            await database_session.execute(
                text("SELECT id FROM subcategories ORDER BY created_at LIMIT 1")
            )
        ).scalar_one()

        result = await catalog_query_service.get_subcategory_attributes(subcategory_id)

        assert result is not None
