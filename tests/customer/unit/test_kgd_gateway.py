import httpx
import pytest

from src.core.customer.domain.enums import Kind
from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError
from src.core.customer.infrastructure.gateways.kgd import NOT_FOUND_MESSAGE, KGDTaxpayerGateway

TAX_ID = "180240041089"


def taxpayer(code: str = TAX_ID, name: str | None = 'ТОО "Olzha Agro"', end_date: str | None = None) -> dict:
    return {"code": code, "messageResult": "SUCCESS", "name": name, "endDate": end_date}


def make_gateway(handler) -> tuple[KGDTaxpayerGateway, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def recording_handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return handler(request)

    gateway = KGDTaxpayerGateway(portal_token="test-token")
    gateway._client = httpx.AsyncClient(
        transport=httpx.MockTransport(recording_handler),
        headers=gateway._client.headers,
    )
    return gateway, requests


def json_response(payload: dict, status_code: int = 200):
    return lambda request: httpx.Response(status_code, json=payload)


class TestKGDTaxpayerGateway:
    @pytest.mark.unit
    @pytest.mark.parametrize(("kind", "taxpayer_type"), [(Kind.COMPANY, "UL"), (Kind.INDIVIDUAL, "IP")])
    async def test_sends_token_code_and_type(self, kind, taxpayer_type):
        gateway, requests = make_gateway(json_response({"taxpayerPortalSearchResponses": [taxpayer()]}))

        await gateway.fetch(kind, TAX_ID)

        request = requests[0]
        assert request.headers["X-Portal-Token"] == "test-token"
        assert request.url.params["taxpayerCode"] == TAX_ID
        assert request.url.params["taxpayerType"] == taxpayer_type

    @pytest.mark.unit
    async def test_maps_active_taxpayer(self):
        gateway, _ = make_gateway(json_response({"taxpayerPortalSearchResponses": [taxpayer()]}))

        result = await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert result.tax_id == TAX_ID
        assert result.legal_name == 'ТОО "Olzha Agro"'
        assert result.kind == Kind.COMPANY
        assert result.is_active is True

    @pytest.mark.unit
    async def test_end_date_means_inactive(self):
        gateway, _ = make_gateway(
            json_response({"taxpayerPortalSearchResponses": [taxpayer(end_date="2020-01-01T00:00:00")]})
        )

        result = await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert result.is_active is False

    @pytest.mark.unit
    async def test_not_found_error_response_returns_none(self):
        payload = {"errorResponse": {"code": TAX_ID, "errorMessage": NOT_FOUND_MESSAGE}}
        gateway, _ = make_gateway(json_response(payload))

        assert await gateway.fetch(Kind.COMPANY, TAX_ID) is None

    @pytest.mark.unit
    async def test_other_error_response_means_unavailable(self):
        payload = {"errorResponse": {"code": TAX_ID, "errorMessage": "Сервис временно недоступен"}}
        gateway, _ = make_gateway(json_response(payload))

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    async def test_not_found_for_another_code_means_unavailable(self):
        payload = {"errorResponse": {"code": "000000000000", "errorMessage": NOT_FOUND_MESSAGE}}
        gateway, _ = make_gateway(json_response(payload))

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    async def test_http_500_means_unavailable(self):
        # KGD answers 500 even for a malformed code; the 12-digit DTO check prevents that case.
        gateway, _ = make_gateway(json_response({"status": 500}, status_code=500))

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    async def test_network_error_means_unavailable(self):
        def handler(request):
            raise httpx.ConnectError("refused", request=request)

        gateway, _ = make_gateway(handler)

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "payload",
        [
            {"taxpayerPortalSearchResponses": []},
            {"taxpayerPortalSearchResponses": [taxpayer(code="999999999999")]},
            {"taxpayerPortalSearchResponses": [taxpayer(name=None)]},
        ],
    )
    async def test_unexpected_shape_means_unavailable(self, payload):
        gateway, _ = make_gateway(json_response(payload))

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)
