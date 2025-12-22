from src.api.references.dto import RoubricResponse
from src.core.references.application.abstract_reference_query_context import AbstractReferenceQueryContext


class GetCategoriesTreeUseCase:
    def __init__(self, query_service: AbstractReferenceQueryContext):
        self.query_service = query_service

    async def execute(self):
        async with self.query_service as query:
            tree = await query.category.get_category_tree()
            return tree

