import uuid
import pytest

from src.core.vendor.domain.entities import Vendor


class TestVendorRepository:

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_and_get_by_id(self, vendor_repository, create_vendor):
        vendor = create_vendor
        result = await vendor_repository.get_by_id(vendor.id)

        assert result is not None
        assert result.id == vendor.id
        assert isinstance(result, Vendor)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_by_tax_id(self, vendor_repository, create_vendor):
        vendor = create_vendor
        result = await vendor_repository.get_by_tax_id(vendor.tax_id.value)

        assert result is not None
        assert result.tax_id.value == vendor.tax_id.value

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_by_account_id(self, vendor_repository, create_vendor):
        vendor = create_vendor
        result = await vendor_repository.get_by_account_id(vendor.account_id)

        assert result is not None
        assert result.account_id == vendor.account_id

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_by_id_returns_none_for_unknown(self, vendor_repository):
        result = await vendor_repository.get_by_id(uuid.uuid4())
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_by_tax_id_returns_none_for_unknown(self, vendor_repository):
        result = await vendor_repository.get_by_tax_id("000000000000")
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_save_updates_existing_vendor(self, vendor_repository, create_vendor):
        vendor = create_vendor
        vendor.change_shop_name("Новое название")
        await vendor_repository.save(vendor)

        updated = await vendor_repository.get_by_id(vendor.id)
        assert updated.shop_name == "Новое название"