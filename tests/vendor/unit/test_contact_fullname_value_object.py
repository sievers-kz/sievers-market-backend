import pytest

from src.core.vendor.domain.exceptions import (
    ContactFullnameFormatError,
    ContactFullnameRequiredError,
)
from src.core.vendor.domain.value_objects import ContactFullname


class TestContactFullnameValueObject:
    @pytest.mark.unit
    def test_success_contact_fullname_creation(self):
        fullname = ContactFullname(
            contact_last_name="Test",
            contact_first_name="Test",
            contact_patronymic="Test",
        )

        assert fullname is not None
        assert fullname.contact_last_name == "Test"

    @pytest.mark.parametrize(
        "contact_last_name, " "contact_first_name", [("", "Test"), ("Test", "")]
    )
    @pytest.mark.unit
    def test_contact_fullname_required_fields_raises(
        self, contact_last_name, contact_first_name
    ):
        with pytest.raises(ContactFullnameRequiredError):
            ContactFullname(
                contact_last_name=contact_last_name,
                contact_first_name=contact_first_name,
            )

    @pytest.mark.parametrize(
        "contact_last_name," "contact_first_name," "contact_patronymic",
        [
            ("Test123", "Test", "Test"),
            ("Test", "Test321", "Test"),
            ("Test", "Test", "Test231"),
        ],
    )
    @pytest.mark.unit
    def test_contact_fullname_invalid_format_raises(
        self, contact_last_name, contact_first_name, contact_patronymic
    ):
        with pytest.raises(ContactFullnameFormatError):
            ContactFullname(
                contact_last_name=contact_last_name,
                contact_first_name=contact_first_name,
                contact_patronymic=contact_patronymic,
            )
