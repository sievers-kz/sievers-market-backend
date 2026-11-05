import pytest

from src.core.customer.domain.exceptions import (
    FullnameRequiredError,
    InvalidFullnameFormatError,
)
from src.core.customer.domain.value_objects import Fullname


class TestCustomerFullnameValueObject:
    @pytest.mark.unit
    def test_success_fullname_creation(self):
        fullname = Fullname(last_name="Testov", first_name="Test", patronymic="Testovich")
        assert fullname.last_name == "Testov"
        assert fullname.patronymic is not None

    @pytest.mark.unit
    def test_fullname_required_fields_raises(self):
        with pytest.raises(FullnameRequiredError):
            Fullname(last_name=None, first_name="Test", patronymic="Testovich")

    @pytest.mark.unit
    def test_fullname_with_wrong_format(self):
        with pytest.raises(InvalidFullnameFormatError):
            Fullname(last_name="Testov123", first_name="Test321", patronymic="Testovich")

    @pytest.mark.unit
    def test_fullname_accepts_kazakh_letters(self):
        fullname = Fullname(last_name="Нұрсұлтанов", first_name="Қайрат", patronymic="Әліұлы")
        assert fullname.first_name == "Қайрат"

    @pytest.mark.parametrize(
        "last_name, first_name, patronymic, field",
        [
            ("Testov", "Test1", None, "first_name"),
            ("Testov1", "Test", None, "last_name"),
            ("Testov", "Test", "Testovich1", "patronymic"),
        ],
    )
    @pytest.mark.unit
    def test_invalid_format_error_names_the_request_field(self, last_name, first_name, patronymic, field):
        with pytest.raises(InvalidFullnameFormatError) as exc_info:
            Fullname(last_name=last_name, first_name=first_name, patronymic=patronymic)
        assert exc_info.value.metadata == {"field": field}

    @pytest.mark.parametrize(
        "last_name, first_name, field", [(None, "Test", "last_name"), ("Testov", None, "first_name")]
    )
    @pytest.mark.unit
    def test_required_error_names_the_request_field(self, last_name, first_name, field):
        with pytest.raises(FullnameRequiredError) as exc_info:
            Fullname(last_name=last_name, first_name=first_name, patronymic=None)
        assert exc_info.value.metadata == {"field": field}
