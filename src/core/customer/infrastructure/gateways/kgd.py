import httpx
from loguru import logger
from pydantic import Field

from src.core.customer.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.customer.domain.enums import Kind
from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError
from src.core.customer.presentation.dto import TaxpayerResponse
from src.core.shared.presentation.dto import DTO

NOT_FOUND_MESSAGE = "Не найдена информация о регистрационном учете налогоплательщика"

TAXPAYER_TYPE_BY_KIND = {
    Kind.COMPANY: "UL",
    Kind.INDIVIDUAL: "IP",
}


class KGDTaxpayer(DTO):
    code: str
    message_result: str = Field(alias="messageResult")
    name: str | None = None
    end_date: str | None = Field(default=None, alias="endDate")


class KGDError(DTO):
    code: str
    error_message: str = Field(alias="errorMessage")


class KGDResponse(DTO):
    taxpayers: list[KGDTaxpayer] = Field(default_factory=list, alias="taxpayerPortalSearchResponses")
    error: KGDError | None = Field(default=None, alias="errorResponse")


class KGDTaxpayerGateway(ITaxpayerGateway):
    TAXPAYER_URL = "https://portal.kgd.gov.kz/services/isnaportalsync/public/taxpayer-data"

    def __init__(self, portal_token: str) -> None:
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(15.0),
            headers={"X-Portal-Token": portal_token},
        )

    async def fetch(self, kind: Kind, tax_id: str) -> TaxpayerResponse | None:
        params = {
            "taxpayerCode": tax_id,
            "taxpayerType": TAXPAYER_TYPE_BY_KIND[kind],
            "print": "false",
        }

        try:
            response = await self._client.get(self.TAXPAYER_URL, params=params)
            response.raise_for_status()
            parsed = KGDResponse.model_validate(response.json())
        except httpx.HTTPStatusError as exc:
            logger.error(
                "KGD HTTP error | status={} body={}",
                exc.response.status_code,
                exc.response.text[:500],
            )
            raise TaxpayerRegistryUnavailableError() from exc
        except (httpx.RequestError, ValueError) as exc:
            logger.error("KGD request/parse error | error={}", exc)
            raise TaxpayerRegistryUnavailableError() from exc

        if parsed.error is not None:
            if parsed.error.code == tax_id and NOT_FOUND_MESSAGE in parsed.error.error_message:
                return None  # КГД ответил: такого нет
            logger.error("KGD unknown error response | message={}", parsed.error.error_message)
            raise TaxpayerRegistryUnavailableError()

        taxpayer = next(
            (t for t in parsed.taxpayers if t.code == tax_id and t.message_result == "SUCCESS"),
            None,
        )
        if taxpayer is None or not taxpayer.name:
            logger.error("KGD unexpected response shape")
            raise TaxpayerRegistryUnavailableError()

        return TaxpayerResponse(
            tax_id=taxpayer.code,
            legal_name=taxpayer.name,
            kind=kind,
            is_active=taxpayer.end_date is None,
        )
