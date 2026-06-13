import pytest

from src.core.iam.domain.exceptions import (
    EmailRequiredError,
    InvalidEmailFormatError,
    PasswordRequiredError,
)
from src.core.iam.domain.value_objects import Email, Password


class TestEmailValueObject:
    @pytest.mark.unit
    def test_successful_email_creation(self):
        email = Email(value="test@example.com")
        assert email.value == "test@example.com"

    @pytest.mark.unit
    def test_email_required_raises(self):
        with pytest.raises(EmailRequiredError):
            Email(value=None)

    @pytest.mark.unit
    def test_email_format_raises(self):
        with pytest.raises(InvalidEmailFormatError):
            Email(value="test")


class TestPasswordValueObject:
    @pytest.mark.unit
    def test_successful_password_creation(self):
        password = Password(value="hashed_password")
        assert password.value is not None

    @pytest.mark.unit
    def test_password_required_raises(self):
        with pytest.raises(PasswordRequiredError):
            Password(value=None)
