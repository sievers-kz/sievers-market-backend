import pytest

from src.core.listing.presentation.contact_masking import mask_email, mask_phone


class TestMaskPhone:
    @pytest.mark.parametrize(
        "phone, expected",
        [
            ("+77472006243", "+7 747 2•• •• ••"),
            ("87472006243", "+7 747 2•• •• ••"),
            ("+7 (747) 200-62-43", "+7 747 2•• •• ••"),
        ],
    )
    def test_kazakhstan_number_is_formatted(self, phone, expected):
        assert mask_phone(phone) == expected

    def test_other_number_keeps_first_four_digits(self):
        assert mask_phone("+998901234567") == "+9989••••••••"

    def test_short_number_still_hides_digits(self):
        assert mask_phone("1234") == "+1234•••"

    @pytest.mark.parametrize("phone", [None, "", "   ", "abc"])
    def test_empty_gives_none(self, phone):
        assert mask_phone(phone) is None


class TestMaskEmail:
    def test_keeps_first_letter_and_domain(self):
        assert mask_email("sales@olzha-agro.kz") == "s••••@olzha-agro.kz"

    def test_one_letter_local_part(self):
        assert mask_email("a@example.com") == "a••••@example.com"

    @pytest.mark.parametrize("email", ["not-an-email", "@example.com", "user@"])
    def test_malformed_is_fully_hidden(self, email):
        assert mask_email(email) == "••••"

    @pytest.mark.parametrize("email", [None, "", "  "])
    def test_empty_gives_none(self, email):
        assert mask_email(email) is None
