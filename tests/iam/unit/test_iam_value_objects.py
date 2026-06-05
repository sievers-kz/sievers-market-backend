import pytest

from src.core.iam.domain.value_objects import Email


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


