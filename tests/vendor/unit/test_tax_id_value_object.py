import pytest

from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.domain.exceptions import InvalidTaxNumberError
from src.core.vendor.domain.value_objects import TaxID


class TestTaxIDValueObject:
    @pytest.mark.unit
    def test_success_iin_creation(self):
        tax_id = TaxID(value="020716550967", type=LegalForm.IE)
        assert tax_id.value == "020716550967"

    @pytest.mark.unit
    def test_success_bin_creation(self):
        tax_id = TaxID(value="180240041089", type=LegalForm.LLP)
        assert tax_id.value == "180240041089"

    @pytest.mark.parametrize("tax_id", [
        "123456789",    # меньше 12 символов
        "adcdefg",      # не цифры
        "1234567890123" # больше 12 символов
    ])
    @pytest.mark.unit
    def test_tax_id_invalid_format_raises(self, tax_id):
        with pytest.raises(InvalidTaxNumberError):
            TaxID(value=tax_id, type=LegalForm.IE)

    @pytest.mark.unit
    def test_tax_id_invalid_checksum_raises(self):
        with pytest.raises(InvalidTaxNumberError):
            TaxID(value="020716550968", type=LegalForm.IE)  # последняя цифра изменена

    @pytest.mark.parametrize("tax_id", [
        "999999550967",  # невалидная дата рождения
        "020716950967",  # 7я цифра не в (1-6)
    ])
    @pytest.mark.unit
    def test_iin_invalid_structure_raises(self, tax_id):
        with pytest.raises(InvalidTaxNumberError):
            TaxID(value=tax_id, type=LegalForm.IE)

    @pytest.mark.parametrize("tax_id", [
        "180013041089",  # месяц 00 — невалидный
        "180240141089",  # 5я цифра не в (4,5,6)
    ])
    @pytest.mark.unit
    def test_bin_invalid_structure_raises(self, tax_id):
        with pytest.raises(InvalidTaxNumberError):
            TaxID(value=tax_id, type=LegalForm.LLP)
