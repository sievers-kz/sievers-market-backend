from src.api.references.dto import RoubricResponse
from src.core.references.application.abstract_reference_uow import AbstractReferenceUnitOfWork


class GetCategoriesTreeUseCase:
    def __init__(self, unit_of_work: AbstractReferenceUnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self):
        async with self.unit_of_work as uow:
            tree = await uow.reference.get_categories_tree()
            return tree

