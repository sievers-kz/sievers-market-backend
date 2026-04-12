import pytest

from src.core.iam.domain.value_objects import Email, Phone


class TestEmailValueObject:
    @pytest.mark.unit
    def test_successful_email_creation(self):
        email = Email(value="test@example.com")
        assert email.value == "test@example.com"

    @pytest.mark.unit
    def test_email_required_raises(self):
        with pytest.raises(ValueError, match="Email обязателен"):
            Email(value=None)

    @pytest.mark.unit
    def test_email_format_raises(self):
        with pytest.raises(ValueError, match="Неправильный формат email"):
            Email(value="test")


class TestPhoneValueObject:
    @pytest.mark.unit
    def test_successful_phone_creation(self):
        phone = Phone(value="+77472006243")
        assert phone.value == "+77472006243"
        assert phone is not None

    @pytest.mark.unit
    def test_phone_format_raises(self):
        with pytest.raises(ValueError, match="Неправильный формат номера телефона"):
            Phone(value="123456789")
