import pytest

from src.core.shared.domain.enums import ListingStatus, PriceCurrency
from tests.machinery.conftest import create_domain_machinery


class TestMachineryAggregate:
    @pytest.mark.unit
    def test_deactivate_success(self):
        machinery = create_domain_machinery()
        machinery.deactivate()
        assert machinery.status == ListingStatus.INACTIVE

    @pytest.mark.unit
    def test_already_deactivated(self):
        machinery = create_domain_machinery()
        machinery.deactivate()
        with pytest.raises(ValueError, match="Объявление уже деактивировано"):
            machinery.deactivate()

    @pytest.mark.unit
    def test_archive_success(self):
        machinery = create_domain_machinery()
        machinery.archive()
        assert machinery.status == ListingStatus.ARCHIVED

    @pytest.mark.unit
    def test_delete_success(self):
        machinery = create_domain_machinery()
        machinery.delete()
        assert machinery.status == ListingStatus.DELETED

    @pytest.mark.unit
    def test_activate_already_active_raises(self):
        machinery = create_domain_machinery()
        with pytest.raises(ValueError, match="Объявление уже активировано"):
            machinery.activate()

    @pytest.mark.unit
    def test_change_description(self):
        machinery = create_domain_machinery()
        machinery.change_description("New test description")
        assert machinery.description.value == "New test description"

    @pytest.mark.unit
    def test_change_price(self):
        machinery = create_domain_machinery()
        machinery.change_price(1_000_000, PriceCurrency.USD)
        assert machinery.price.value == 1_000_000
        assert machinery.currency == PriceCurrency.USD

