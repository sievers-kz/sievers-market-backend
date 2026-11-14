import uuid

import pytest

from src.core.customer.domain.entities import Organization
from src.core.customer.domain.enums import Kind, RegistryStatus
from src.core.customer.domain.exceptions import (
    InvalidShopNameError,
    OrganizationCannotPublishError,
    OrganizationNotFoundError,
    OrganizationProfileIncompleteError,
)


def make_organization() -> Organization:
    return Organization.create(owner_id=uuid.uuid4(), tax_id="180240041089", kind=Kind.COMPANY)


def make_publishable_organization() -> Organization:
    organization = make_organization()
    organization.mark_registry_verified("ТОО")
    organization.change_shop_name("Olzha Agro")
    organization.change_contact_phone("+77001234567")
    organization.change_contact_email("shop@example.com")
    return organization


class TestOrganizationEntity:
    @pytest.mark.unit
    def test_create_starts_pending_and_unverified(self):
        organization = make_organization()

        assert organization.registry_status == RegistryStatus.PENDING
        assert organization.is_ownership_verified is False
        assert organization.legal_name is None
        assert organization.tax_id == "180240041089"
        assert organization.kind == Kind.COMPANY

    @pytest.mark.unit
    def test_create_generates_unique_ids(self):
        assert make_organization().id != make_organization().id

    @pytest.mark.unit
    def test_mark_registry_verified_sets_status_and_legal_name(self):
        organization = make_organization()

        organization.mark_registry_verified('ТОО "Olzha Agro"')

        assert organization.registry_status == RegistryStatus.VERIFIED
        assert organization.legal_name == 'ТОО "Olzha Agro"'

    @pytest.mark.unit
    def test_mark_registry_verified_stores_legal_address(self):
        organization = make_organization()

        organization.mark_registry_verified('ТОО "Olzha Agro"', "Г.АСТАНА, УЛИЦА БАРАЕВ, ЗДАНИЕ 16")

        assert organization.legal_address == "Г.АСТАНА, УЛИЦА БАРАЕВ, ЗДАНИЕ 16"

    @pytest.mark.unit
    def test_mark_registry_verified_without_address_keeps_it_empty(self):
        organization = make_organization()

        organization.mark_registry_verified('ТОО "Olzha Agro"')

        assert organization.legal_address is None

    @pytest.mark.unit
    def test_mark_registry_not_found_keeps_legal_name_empty(self):
        organization = make_organization()

        organization.mark_registry_not_found()

        assert organization.registry_status == RegistryStatus.NOT_FOUND
        assert organization.legal_name is None

    @pytest.mark.unit
    def test_is_owned_by(self):
        organization = make_organization()

        assert organization.is_owned_by(organization.owner_id) is True
        assert organization.is_owned_by(uuid.uuid4()) is False

    @pytest.mark.unit
    def test_ensure_can_publish_passes_for_owner_of_verified_with_profile(self):
        organization = make_publishable_organization()

        organization.ensure_can_publish(organization.owner_id)

    @pytest.mark.unit
    def test_ensure_can_publish_hides_foreign_organization(self):
        organization = make_publishable_organization()

        with pytest.raises(OrganizationNotFoundError):
            organization.ensure_can_publish(uuid.uuid4())

    @pytest.mark.unit
    @pytest.mark.parametrize("status", [RegistryStatus.PENDING, RegistryStatus.NOT_FOUND])
    def test_ensure_can_publish_rejects_unverified(self, status):
        organization = make_organization()
        organization.registry_status = status

        with pytest.raises(OrganizationCannotPublishError):
            organization.ensure_can_publish(organization.owner_id)

    @pytest.mark.unit
    @pytest.mark.parametrize("field", ["shop_name", "contact_phone", "contact_email"])
    def test_ensure_can_publish_rejects_missing_profile_field(self, field):
        organization = make_publishable_organization()
        setattr(organization, field, None)

        with pytest.raises(OrganizationProfileIncompleteError) as error:
            organization.ensure_can_publish(organization.owner_id)

        assert error.value.metadata == {"missing_fields": [field]}

    @pytest.mark.unit
    def test_ensure_can_publish_reports_unverified_before_missing_profile(self):
        organization = make_organization()

        with pytest.raises(OrganizationCannotPublishError):
            organization.ensure_can_publish(organization.owner_id)

    @pytest.mark.unit
    def test_change_shop_name_stores_trimmed_name_with_collapsed_spaces(self):
        organization = make_organization()

        organization.change_shop_name("  Olzha   Agro  ")

        assert organization.shop_name == "Olzha Agro"

    @pytest.mark.unit
    @pytest.mark.parametrize("shop_name", ["", "   ", "A", "12345", "---", "x" * 51])
    def test_change_shop_name_rejects_invalid_name(self, shop_name):
        organization = make_organization()

        with pytest.raises(InvalidShopNameError):
            organization.change_shop_name(shop_name)

        assert organization.shop_name is None

    @pytest.mark.unit
    @pytest.mark.parametrize("shop_name", ["Ол", "x" * 50, "Агро 24"])
    def test_change_shop_name_accepts_boundaries(self, shop_name):
        organization = make_organization()

        organization.change_shop_name(shop_name)

        assert organization.shop_name == shop_name

    @pytest.mark.unit
    def test_change_contact_phone_and_email(self):
        organization = make_organization()

        organization.change_contact_phone("+77011234567")
        organization.change_contact_email("shop@example.com")

        assert organization.contact_phone == "+77011234567"
        assert organization.contact_email == "shop@example.com"
