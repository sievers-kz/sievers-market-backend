import pytest
from pydantic import ValidationError

from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.customer.domain.exceptions import OrganizationAlreadyExistsError
from src.core.customer.presentation.dto import CreateOrganizationRequest
from src.core.shared.infrastructure.tasks import TaskNames
from tests.customer.conftest import random_tax_id


class TestCreateOrganizationUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_creates_pending_organization(self, create_organization_usecase, create_customer, get_organization):
        dto = CreateOrganizationRequest(kind=Kind.COMPANY, tax_id=random_tax_id())

        response = await create_organization_usecase.execute(create_customer.id, dto)

        assert response.registry_status == RegistryStatus.PENDING
        organization = await get_organization(response.id)
        assert organization is not None
        assert organization.owner_id == create_customer.id
        assert organization.tax_id == dto.tax_id
        assert organization.kind == Kind.COMPANY
        assert organization.registry_status == RegistryStatus.PENDING

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_enqueues_verification_task(self, create_organization_usecase, create_customer, mock_arq):
        dto = CreateOrganizationRequest(kind=Kind.COMPANY, tax_id=random_tax_id())

        response = await create_organization_usecase.execute(create_customer.id, dto)

        mock_arq.enqueue.assert_awaited_once_with(
            task_name=TaskNames.VERIFY_ORGANIZATION_REGISTRY,
            organization_id=str(response.id),
        )

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_duplicate_tax_id_raises_and_does_not_enqueue(
        self, create_organization_usecase, create_customer, mock_arq
    ):
        dto = CreateOrganizationRequest(kind=Kind.COMPANY, tax_id=random_tax_id())
        await create_organization_usecase.execute(create_customer.id, dto)
        mock_arq.enqueue.reset_mock()

        with pytest.raises(OrganizationAlreadyExistsError):
            await create_organization_usecase.execute(create_customer.id, dto)

        mock_arq.enqueue.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_queue_failure_still_returns_pending_organization(
        self, create_organization_usecase, create_customer, mock_arq, get_organization
    ):
        # Redis is down: the organization is already committed and stays PENDING for the cron to pick up.
        mock_arq.enqueue.side_effect = ConnectionError("redis down")
        dto = CreateOrganizationRequest(kind=Kind.COMPANY, tax_id=random_tax_id())

        response = await create_organization_usecase.execute(create_customer.id, dto)

        assert response.registry_status == RegistryStatus.PENDING
        assert (await get_organization(response.id)).registry_status == RegistryStatus.PENDING

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_customer_can_own_several_organizations(
        self, create_organization_usecase, create_customer, get_organization
    ):
        first = await create_organization_usecase.execute(
            create_customer.id, CreateOrganizationRequest(kind=Kind.COMPANY, tax_id=random_tax_id())
        )
        second = await create_organization_usecase.execute(
            create_customer.id, CreateOrganizationRequest(kind=Kind.INDIVIDUAL, tax_id=random_tax_id())
        )

        assert first.id != second.id
        assert await get_organization(first.id) is not None
        assert await get_organization(second.id) is not None


class TestCreateOrganizationRequest:
    @pytest.mark.unit
    @pytest.mark.parametrize("tax_id", ["12345", "1234567890123", "18024004108a", "", "18024004108 "])
    def test_rejects_tax_id_that_is_not_12_digits(self, tax_id):
        with pytest.raises(ValidationError):
            CreateOrganizationRequest(kind=Kind.COMPANY, tax_id=tax_id)

    @pytest.mark.unit
    def test_accepts_12_digits(self):
        assert CreateOrganizationRequest(kind=Kind.COMPANY, tax_id="180240041089").tax_id == "180240041089"
