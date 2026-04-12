import pytest

from src.core.shared.domain.enums import ListingStatus


class TestArchiveMachineryUsecase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_archive_machinery_successful(
        self,
        create_machinery_usecase,
        archive_machinery_usecase,
        machinery_repository,
        create_machinery_request,
        create_customer
    ):
        dto = create_machinery_request
        machinery_id = await create_machinery_usecase.execute(create_customer.id, dto)

        await archive_machinery_usecase.execute(create_customer.id, machinery_id)
        machinery = await machinery_repository.get_machinery_by_id(machinery_id)

        assert machinery is not None
        assert machinery.status == ListingStatus.ARCHIVED
        