import uuid

import pytest

from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError
from tests.customer.conftest import create_domain_organization, create_taxpayer


@pytest.fixture
def pending_organization(create_customer, save_organization):
    async def _create(kind: Kind = Kind.COMPANY, registry_status: RegistryStatus = RegistryStatus.PENDING):
        organization = create_domain_organization(
            owner_id=create_customer.id, kind=kind, registry_status=registry_status
        )
        return await save_organization(organization)

    return _create


class TestVerifyOrganizationRegistryUseCase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_marks_verified_and_stores_legal_name(
        self, verify_organization_registry_usecase, mock_taxpayer_gateway, pending_organization, get_organization
    ):
        organization = await pending_organization()
        mock_taxpayer_gateway.fetch.return_value = create_taxpayer(organization.tax_id, legal_name='ТОО "Родина"')

        await verify_organization_registry_usecase.execute(organization.id)

        result = await get_organization(organization.id)
        assert result.registry_status == RegistryStatus.VERIFIED
        assert result.legal_name == 'ТОО "Родина"'
        mock_taxpayer_gateway.fetch.assert_awaited_once_with(Kind.COMPANY, organization.tax_id)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_marks_not_found_when_registry_has_no_record(
        self, verify_organization_registry_usecase, mock_taxpayer_gateway, pending_organization, get_organization
    ):
        organization = await pending_organization()
        mock_taxpayer_gateway.fetch.return_value = None

        await verify_organization_registry_usecase.execute(organization.id)

        result = await get_organization(organization.id)
        assert result.registry_status == RegistryStatus.NOT_FOUND
        assert result.legal_name is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_marks_not_found_when_kind_mismatches(
        self, verify_organization_registry_usecase, mock_taxpayer_gateway, pending_organization, get_organization
    ):
        organization = await pending_organization(kind=Kind.INDIVIDUAL)
        mock_taxpayer_gateway.fetch.return_value = create_taxpayer(organization.tax_id, kind=Kind.COMPANY)

        await verify_organization_registry_usecase.execute(organization.id)

        assert (await get_organization(organization.id)).registry_status == RegistryStatus.NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_marks_not_found_when_taxpayer_inactive(
        self, verify_organization_registry_usecase, mock_taxpayer_gateway, pending_organization, get_organization
    ):
        organization = await pending_organization()
        mock_taxpayer_gateway.fetch.return_value = create_taxpayer(organization.tax_id, is_active=False)

        await verify_organization_registry_usecase.execute(organization.id)

        assert (await get_organization(organization.id)).registry_status == RegistryStatus.NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_registry_unavailable_raises_and_keeps_pending(
        self, verify_organization_registry_usecase, mock_taxpayer_gateway, pending_organization, get_organization
    ):
        organization = await pending_organization()
        mock_taxpayer_gateway.fetch.side_effect = TaxpayerRegistryUnavailableError()

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await verify_organization_registry_usecase.execute(organization.id)

        assert (await get_organization(organization.id)).registry_status == RegistryStatus.PENDING

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_missing_organization_exits_quietly(
        self, verify_organization_registry_usecase, mock_taxpayer_gateway
    ):
        await verify_organization_registry_usecase.execute(uuid.uuid4())

        mock_taxpayer_gateway.fetch.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("status", [RegistryStatus.VERIFIED, RegistryStatus.NOT_FOUND])
    async def test_already_processed_organization_is_left_untouched(
        self,
        status,
        verify_organization_registry_usecase,
        mock_taxpayer_gateway,
        pending_organization,
        get_organization,
    ):
        organization = await pending_organization(registry_status=status)

        await verify_organization_registry_usecase.execute(organization.id)

        mock_taxpayer_gateway.fetch.assert_not_awaited()
        assert (await get_organization(organization.id)).registry_status == status

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_organization_deleted_during_registry_call_exits_quietly(
        self,
        verify_organization_registry_usecase,
        mock_taxpayer_gateway,
        pending_organization,
        customer_uow,
        get_organization,
    ):
        organization = await pending_organization()

        async def delete_then_answer(kind, tax_id):
            async with customer_uow as uow:
                await uow.organization.delete(organization.id)
                await uow.commit()
            return create_taxpayer(tax_id)

        mock_taxpayer_gateway.fetch.side_effect = delete_then_answer

        await verify_organization_registry_usecase.execute(organization.id)

        assert await get_organization(organization.id) is None
