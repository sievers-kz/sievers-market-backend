from enum import StrEnum

import httpx
from loguru import logger

from src.core.customer.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.customer.domain.enums import Kind
from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError
from src.core.customer.presentation.dto import TaxpayerResponse
from src.core.shared.presentation.dto import DTO


class DaDataType(StrEnum):
    LEGAL = "LEGAL"
    BRANCH = "BRANCH"
    FOREIGN_BRANCH = "FOREIGN_BRANCH"
    INDIVIDUAL = "INDIVIDUAL"
    INDIVIDUAL_JOINT_VENTURE = "INDIVIDUAL_JOINT_VENTURE"


class DaDataStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LIQUIDATING = "LIQUIDATING"
    LIQUIDATED = "LIQUIDATED"
    SUSPENDED = "SUSPENDED"


class DaDataParty(DTO):
    bin: str
    type: DaDataType
    status: DaDataStatus
    name_ru: str


class DaDataSuggestion(DTO):
    data: DaDataParty


class DaDataResponse(DTO):
    suggestions: list[DaDataSuggestion]


KIND_DADATA_BY_TYPE = {
    DaDataType.LEGAL: Kind.COMPANY,
    DaDataType.BRANCH: Kind.COMPANY,
    DaDataType.FOREIGN_BRANCH: Kind.COMPANY,
    DaDataType.INDIVIDUAL: Kind.INDIVIDUAL,
    DaDataType.INDIVIDUAL_JOINT_VENTURE: Kind.INDIVIDUAL,
}


class DaDataTaxpayerGateway(ITaxpayerGateway):
    FIND_BY_ID_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party_kz"

    def __init__(self, api_key: str) -> None:
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
            headers={
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

    async def fetch(self, kind: Kind, tax_id: str) -> TaxpayerResponse | None:
        try:
            response = await self._client.post(self.FIND_BY_ID_URL, json={"query": tax_id})
            response.raise_for_status()
            parsed = DaDataResponse.model_validate(response.json())
        except httpx.HTTPStatusError as exc:
            logger.error(
                "DaData HTTP error | status={} body={}",
                exc.response.status_code,
                exc.response.text[:500],
            )
            raise TaxpayerRegistryUnavailableError() from exc
        except (httpx.RequestError, ValueError) as exc:
            logger.error("DaData request/parse error | error={}", exc)
            raise TaxpayerRegistryUnavailableError() from exc

        party = next((s.data for s in parsed.suggestions if s.data.bin == tax_id), None)
        if party is None:
            return None

        return TaxpayerResponse(
            tax_id=party.bin,
            legal_name=party.name_ru,
            kind=KIND_DADATA_BY_TYPE[party.type],
            is_active=party.status is DaDataStatus.ACTIVE,
        )
