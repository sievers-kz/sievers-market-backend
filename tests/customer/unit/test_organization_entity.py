import uuid

import pytest

from src.core.customer.domain.entities import Organization
from src.core.customer.domain.enums import Kind, RegistryStatus


def make_organization() -> Organization:
    return Organization.create(owner_id=uuid.uuid4(), tax_id="180240041089", kind=Kind.COMPANY)


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
    def test_mark_registry_not_found_keeps_legal_name_empty(self):
        organization = make_organization()

        organization.mark_registry_not_found()

        assert organization.registry_status == RegistryStatus.NOT_FOUND
        assert organization.legal_name is None

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("status", "expected"),
        [
            (RegistryStatus.PENDING, False),
            (RegistryStatus.NOT_FOUND, False),
            (RegistryStatus.VERIFIED, True),
        ],
    )
    def test_can_publish_only_when_verified(self, status, expected):
        organization = make_organization()
        organization.registry_status = status

        assert organization.can_publish() is expected
