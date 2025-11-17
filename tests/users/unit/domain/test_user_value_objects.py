import pytest

from src.core.users.domain.exceptions.exception_classes import MissingRequiredFieldError, InvalidInputError
from src.core.users.domain.value_objects import Fullname, Email, Phone, OrganizationFullname, DocumentValue


class TestFullnameValueObject:
    @pytest.mark.unit
    def test_fullname_creation_success(self):
        fullname = Fullname.from_raw(
            first_name="Мейржан",
            last_name="Бисенов",
            patronymic="Баскарович"
        )

        assert fullname.first_name == "Мейржан"
        assert fullname.last_name == "Бисенов"
        assert fullname.patronymic == "Баскарович"

    @pytest.mark.unit
    def test_fullname_without_patronymic(self):
        fullname = Fullname.from_raw(
            first_name="Мейржан",
            last_name="Бисенов",
            patronymic=None
        )

        assert fullname.first_name == "Мейржан"
        assert fullname.last_name == "Бисенов"
        assert fullname.patronymic is None

    @pytest.mark.parametrize(
        "first, last, field_name",
        [
            ("", "Бисенов", "first_name"),
            ("Мейржан", "", "last_name")
        ]
    )
    @pytest.mark.unit
    def test_fullname_missing_required_field_fail(self, first, last, field_name):
        with pytest.raises(MissingRequiredFieldError) as excinfo:
            Fullname.from_raw(
                first_name=first,
                last_name=last,
                patronymic="Баскарович"
            )

        assert excinfo.value.meta.context["field"] == field_name

    @pytest.mark.parametrize(
        "field, value", [
            ("first_name", "Meirzhan1"),
            ("last_name", "Bi55enov@"),
            ("patronymic", "Баскарович%")
        ]
    )
    @pytest.mark.unit
    def test_fullname_invalid_format_fail(self, field, value):
        test_data = {"first_name": "Мейржан", "last_name": "Бисенов", "patronymic": "Баскарович"}
        test_data[field] = value

        with pytest.raises(InvalidInputError) as excinfo:
            Fullname.from_raw(**test_data)

        assert excinfo.value.meta.context["field"] == field


class TestEmailValueObject:
    @pytest.mark.unit
    def test_email_creation_success(self):
        email = Email.from_raw(raw_email="test@example.com")
        assert email.value == "test@example.com"

    @pytest.mark.unit
    def test_email_without_value_fail(self):
        raw_email = "" or None
        with pytest.raises(MissingRequiredFieldError) as excinfo:
            Email.from_raw(raw_email=raw_email)

        assert excinfo.value.meta.context["field"] == "email"

    @pytest.mark.parametrize(
        "invalid_email", [
            "not-an-email.com",
            "user@domain",
            "test space@example.com",
            "user@.com"
        ]
    )
    @pytest.mark.unit
    def test_email_invalid_format_fail(self, invalid_email):
        with pytest.raises(InvalidInputError) as excinfo:
            Email.from_raw(raw_email=invalid_email)

        assert excinfo.value.meta.context["field"] == "email"


class TestPhoneValueObject:
    @pytest.mark.unit
    def test_phone_creation_success(self):
        phone = Phone.from_raw(raw_phone="+77472006243")
        assert phone.value == "+77472006243"

    @pytest.mark.unit
    def test_phone_without_value(self):
        phone = Phone.from_raw(raw_phone=None)
        assert phone.value is None

    @pytest.mark.parametrize(
        "invalid_phone", [
            "9472006243",
            "+84472226344",
            "77s24592021",
            "+7472006243"
        ]
    )
    @pytest.mark.unit
    def test_phone_invalid_format(self, invalid_phone):
        with pytest.raises(InvalidInputError) as excinfo:
            Phone.from_raw(raw_phone=invalid_phone)

        assert excinfo.value.meta.context["field"] == "phone"


class TestOrganizationFullnameValueObject:
    @pytest.mark.parametrize(
        "valid_field", [
            "ТОО 'АГРОНОМ'",
            "Индивидуальный Предприниматель Жатка",
            "QAZAGRO (Since 2023)",
            "AGROW (Agriculture - Growth)",
            "QazaqFarm №1"
        ]
    )
    @pytest.mark.unit
    def test_organization_fullname_creation_success(self, valid_field):
        organization_fullname = OrganizationFullname.from_raw(raw_organization_fullname=valid_field)
        assert organization_fullname.value == valid_field

    @pytest.mark.unit
    def test_organization_fullname_without_value(self):
        organization_fullname = None
        with pytest.raises(MissingRequiredFieldError) as excinfo:
            OrganizationFullname.from_raw(raw_organization_fullname=organization_fullname)
        assert excinfo.value.meta.context["field"] == "organization_fullname"

    @pytest.mark.parametrize(
        "invalid_field", [
            "==ТОО Агроном",
            "_ТОО Иероглиф_",
            "ТОО 500$",
            ".ТОО Агроном",
        ]
    )
    @pytest.mark.unit
    def test_organization_fullname_invalid_format_fail(self, invalid_field):
        with pytest.raises(InvalidInputError) as excinfo:
            OrganizationFullname.from_raw(raw_organization_fullname=invalid_field)

        assert excinfo.value.meta.context["field"] == "organization_fullname"


class TestDocumentValueValueObject:
    @pytest.mark.parametrize(
        "valid_document_value", [
            "123456789012",
            "020912550994",
            "071224590213"
        ]
    )
    @pytest.mark.unit
    def test_document_value_success_creation(self, valid_document_value):
        document_value = DocumentValue.from_raw(valid_document_value)
        assert document_value.value == valid_document_value

    @pytest.mark.unit
    def test_document_value_without_field(self):
        document_value = None
        with pytest.raises(MissingRequiredFieldError) as excinfo:
            DocumentValue.from_raw(raw_value=document_value)

        assert excinfo.value.meta.context["field"] == "document_value"

    @pytest.mark.parametrize(
        "invalid_document_value", [
            "123456789123456789",
            "123sss3455fds",
            "%1231sad123"
        ]
    )
    @pytest.mark.unit
    def test_document_value_invalid_format(self, invalid_document_value):
        with pytest.raises(InvalidInputError) as excinfo:
            DocumentValue.from_raw(raw_value=invalid_document_value)

        assert excinfo.value.meta.context["field"] == "document_value"
