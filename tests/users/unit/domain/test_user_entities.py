import uuid

import pytest

from src.core.users.domain.entities import BusinessDetails
from src.core.users.domain.enums import BusinessTypeEnum, DocumentTypeEnum
from src.core.users.domain.exceptions.exception_classes import InvalidInputError
from src.core.users.domain.value_objects import OrganizationFullname, DocumentValue


class TestBusinessDetailsEntity:
    @pytest.mark.unit
    def test_business_details_creation_success(self):
        details = BusinessDetails(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            business_type=BusinessTypeEnum.IP,
            organization_fullname=OrganizationFullname.from_raw("ТОО 'AGROW'"),
            document_type=DocumentTypeEnum.IIN,
            document_value=DocumentValue.from_raw("123456789012")
        )

        assert details.business_type == BusinessTypeEnum.IP
        assert details.document_type == DocumentTypeEnum.IIN

    @pytest.mark.unit
    def test_business_details_ip_with_bin_fail(self):
        with pytest.raises(InvalidInputError) as excinfo:
            BusinessDetails(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                business_type=BusinessTypeEnum.IP,
                organization_fullname=OrganizationFullname.from_raw("ТОО 'AGROW'"),
                document_type=DocumentTypeEnum.BIN,
                document_value=DocumentValue.from_raw("210987654321")
            )

        assert excinfo.value.meta.code == "invalid_document_type_for_individual"
        assert excinfo.value.meta.context["field"] == "document_type"

    @pytest.mark.unit
    def test_business_details_bin_with_iin_fail(self):
        with pytest.raises(InvalidInputError) as excinfo:
            BusinessDetails(
                id=uuid.uuid4(),
                user_id=uuid.uuid4(),
                business_type=BusinessTypeEnum.TOO,
                organization_fullname=OrganizationFullname.from_raw("ТОО 'AGROW'"),
                document_type=DocumentTypeEnum.IIN,
                document_value=DocumentValue.from_raw("210987654321")
            )

        assert excinfo.value.meta.code == "invalid_document_type_for_too"
        assert excinfo.value.meta.context["field"] == "document_type"
