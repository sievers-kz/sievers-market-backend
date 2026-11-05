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

    @pytest.mark.parametrize("contact_last_name, " "contact_first_name", [("", "Test"), ("Test", "")])
    @pytest.mark.unit
    def test_contact_fullname_required_fields_raises(self, contact_last_name, contact_first_name):
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
    def test_contact_fullname_invalid_format_raises(self, contact_last_name, contact_first_name, contact_patronymic):
        with pytest.raises(ContactFullnameFormatError):
            ContactFullname(
                contact_last_name=contact_last_name,
                contact_first_name=contact_first_name,
                contact_patronymic=contact_patronymic,
            )

    @pytest.mark.unit
    def test_contact_fullname_accepts_kazakh_letters(self):
        fullname = ContactFullname(
            contact_last_name="Нұрсұлтанов",
            contact_first_name="Қайрат",
            contact_patronymic="Әліұлы",
        )
        assert fullname.contact_first_name == "Қайрат"

    @pytest.mark.parametrize(
        "contact_last_name, contact_first_name, contact_patronymic, field",
        [
            ("Test1", "Test", None, "contact_last_name"),
            ("Test", "Test1", None, "contact_first_name"),
            ("Test", "Test", "Test1", "contact_patronymic"),
        ],
    )
    @pytest.mark.unit
    def test_format_error_names_the_request_field(
        self, contact_last_name, contact_first_name, contact_patronymic, field
    ):
        with pytest.raises(ContactFullnameFormatError) as exc_info:
            ContactFullname(
                contact_last_name=contact_last_name,
                contact_first_name=contact_first_name,
                contact_patronymic=contact_patronymic,
            )
        assert exc_info.value.metadata == {"field": field}
