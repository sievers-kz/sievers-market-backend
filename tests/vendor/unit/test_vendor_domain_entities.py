from datetime import datetime, timedelta, timezone

import pytest

from src.core.vendor.domain.enums import VendorStatus
from src.core.vendor.domain.exceptions import (
    VendorAlreadyVerifiedError,
    VendorCannotBeRestoredError,
)
from tests.vendor.conftest import create_domain_vendor


class TestVendorEntity:
    @pytest.mark.unit
    def test_create_vendor_success(self):
        vendor = create_domain_vendor()
        assert vendor.is_verified is False
        assert vendor.status == VendorStatus.ACTIVE
        assert vendor.closed_at is None

    @pytest.mark.unit
    def test_verify_success(self):
        vendor = create_domain_vendor()
        vendor.verify()
        assert vendor.is_verified is True

    @pytest.mark.unit
    def test_verify_already_verified_raises(self):
        vendor = create_domain_vendor()
        vendor.verify()
        with pytest.raises(VendorAlreadyVerifiedError):
            vendor.verify()

    @pytest.mark.unit
    def test_close_success(self):
        vendor = create_domain_vendor()
        vendor.close()
        assert vendor.status == VendorStatus.CLOSED
        assert vendor.closed_at is not None

    @pytest.mark.unit
    def test_restore_success(self):
        vendor = create_domain_vendor()
        vendor.close()
        vendor.restore()
        assert vendor.status == VendorStatus.ACTIVE
        assert vendor.closed_at is None

    @pytest.mark.unit
    def test_restore_after_30_days_raises(self):
        vendor = create_domain_vendor()
        vendor.close()
        vendor.closed_at = datetime.now(timezone.utc) - timedelta(days=31)
        with pytest.raises(VendorCannotBeRestoredError):
            vendor.restore()

    @pytest.mark.unit
    def test_restore_banned_vendor_raises(self):
        vendor = create_domain_vendor()
        vendor.ban()
        with pytest.raises(VendorCannotBeRestoredError):
            vendor.restore()

    @pytest.mark.unit
    def test_ban_success(self):
        vendor = create_domain_vendor()
        vendor.ban()
        assert vendor.status == VendorStatus.BANNED

    @pytest.mark.unit
    def test_is_restorable_within_30_days(self):
        vendor = create_domain_vendor()
        vendor.close()
        assert vendor.is_restorable() is True

    @pytest.mark.unit
    def test_is_restorable_after_30_days(self):
        vendor = create_domain_vendor()
        vendor.close()
        vendor.closed_at = datetime.now(timezone.utc) - timedelta(days=31)
        assert vendor.is_restorable() is False
