import uuid

import pytest

from src.core.customer.domain.entities import Organization
from src.core.customer.domain.enums import Kind
from src.core.customer.domain.policies import missing_profile_fields


def make_organization() -> Organization:
    return Organization.create(owner_id=uuid.uuid4(), tax_id="180240041089", kind=Kind.COMPANY)


class TestMissingProfileFields:
    @pytest.mark.unit
    def test_new_organization_misses_all_fields(self):
        assert missing_profile_fields(make_organization()) == ["shop_name", "contact_phone", "contact_email"]

    @pytest.mark.unit
    def test_filled_fields_are_not_reported(self):
        organization = make_organization()
        organization.change_shop_name("Olzha Agro")
        organization.change_contact_email("shop@example.com")

        assert missing_profile_fields(organization) == ["contact_phone"]

    @pytest.mark.unit
    def test_complete_profile_misses_nothing(self):
        organization = make_organization()
        organization.change_shop_name("Olzha Agro")
        organization.change_contact_phone("+77001234567")
        organization.change_contact_email("shop@example.com")

        assert missing_profile_fields(organization) == []
