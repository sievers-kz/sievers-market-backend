import pytest

from src.core.customer.domain.exceptions import (
    FullnameRequiredError,
    InvalidFullnameFormatError,
)
from src.core.customer.domain.value_objects import Fullname


class TestCustomerFullnameValueObject:
    @pytest.mark.unit
    def test_success_fullname_creation(self):
        fullname = Fullname(
            last_name="Testov", first_name="Test", patronymic="Testovich"
        )
        assert fullname.last_name == "Testov"
        assert fullname.patronymic is not None

    @pytest.mark.unit
    def test_fullname_required_fields_raises(self):
        with pytest.raises(FullnameRequiredError):
            Fullname(last_name=None, first_name="Test", patronymic="Testovich")

    @pytest.mark.unit
    def test_fullname_with_wrong_format(self):
        with pytest.raises(InvalidFullnameFormatError):
            Fullname(
                last_name="Testov123", first_name="Test321", patronymic="Testovich"
            )
