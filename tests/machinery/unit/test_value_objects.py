from datetime import datetime

import pytest

from src.core.machinery.domain.value_objects import Title, Price, YearOfIssue, Description


class TestTitleValueObject:
    @pytest.mark.unit
    def test_successful_title_creation(self):
        title = Title(value="John Deere")
        assert title.value == "John Deere"

    @pytest.mark.unit
    def test_composite_title_creation(self):
        title = Title.create(brand_name="John Deere", model="8000R")
        assert "8000R" in title.value

    @pytest.mark.unit
    def test_title_creation_without_model(self):
        title = Title.create(brand_name="John Deere")
        assert title.value == "John Deere"

    @pytest.mark.unit
    def test_title_required_raises(self):
        with pytest.raises(ValueError, match="Заголовок обязательное поле"):
            Title(value="")

    @pytest.mark.unit
    def test_title_too_long_raises(self):
        with pytest.raises(ValueError, match="Заголовок не должен превышать 50 символов"):
            Title(value="X" * 51)


class TestPriceValueObject:
    @pytest.mark.unit
    def test_successful_price_creation(self):
        price = Price(value=1_000_000)
        assert price.value == 1_000_000

    @pytest.mark.unit
    def test_price_required_raises(self):
        with pytest.raises(ValueError, match="Цена обязательное поле"):
            Price(value=None)

    @pytest.mark.unit
    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
            Price(value=-1_000_000)


class TestYearOfIssueValueObject:
    @pytest.mark.unit
    def test_successful_year_creation(self):
        year_of_issue = YearOfIssue(value=2026)
        assert year_of_issue.value == 2026

    @pytest.mark.unit
    def test_year_required_raises(self):
        with pytest.raises(ValueError, match="Год выпуска обязательное поле"):
            YearOfIssue(value=None)

    @pytest.mark.unit
    def test_year_range_raises(self):
        future_year = datetime.now().year + 1
        with pytest.raises(ValueError):
            YearOfIssue(value=future_year)


class TestDescriptionValueObject:
    @pytest.mark.unit
    def test_successful_description_creation(self):
        description = Description(value="Test Description")
        assert description.value == "Test Description"

    @pytest.mark.unit
    def test_too_long_description_raises(self):
        with pytest.raises(ValueError, match="Описание не должно превышать 3000 символов"):
            Description(value="X" * 3001)
