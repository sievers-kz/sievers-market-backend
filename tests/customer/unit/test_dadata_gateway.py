import json

import httpx
import pytest

from src.core.customer.domain.enums import Kind
from src.core.customer.domain.exceptions import TaxpayerRegistryUnavailableError
from src.core.customer.infrastructure.gateways.dadata import DaDataTaxpayerGateway

TAX_ID = "180240041089"


def party(
    bin_: str = TAX_ID,
    type_: str = "LEGAL",
    status: str = "ACTIVE",
    name: str = 'ТОО "Olzha Agro"',
    address: str | None = None,
) -> dict:
    data = {"bin": bin_, "type": type_, "status": status, "name_ru": name}
    if address is not None:
        data["address_ru"] = address
    return {"value": name, "data": data}


def make_gateway(handler) -> tuple[DaDataTaxpayerGateway, list[httpx.Request]]:
    """Gateway whose HTTP client answers through `handler` instead of the network."""
    requests: list[httpx.Request] = []

    def recording_handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return handler(request)

    gateway = DaDataTaxpayerGateway(api_key="test-key")
    gateway._client = httpx.AsyncClient(
        transport=httpx.MockTransport(recording_handler),
        headers=gateway._client.headers,
    )
    return gateway, requests


def json_response(payload: dict, status_code: int = 200):
    return lambda request: httpx.Response(status_code, json=payload)


class TestDaDataTaxpayerGateway:
    @pytest.mark.unit
    async def test_sends_token_and_query(self):
        gateway, requests = make_gateway(json_response({"suggestions": [party()]}))

        await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert requests[0].headers["Authorization"] == "Token test-key"
        assert json.loads(requests[0].content) == {"query": TAX_ID}

    @pytest.mark.unit
    async def test_maps_active_legal_entity(self):
        gateway, _ = make_gateway(json_response({"suggestions": [party()]}))

        result = await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert result is not None
        assert result.tax_id == TAX_ID
        assert result.legal_name == 'ТОО "Olzha Agro"'
        assert result.kind == Kind.COMPANY
        assert result.is_active is True

    @pytest.mark.unit
    async def test_maps_address(self):
        address = "Г.АСТАНА, РАЙОН БАЙҚОҢЫР, МИКРОРАЙОН ЖАСТАР, УЛИЦА АЛЕКСАНДР БАРАЕВ, ЗДАНИЕ 16"
        gateway, _ = make_gateway(json_response({"suggestions": [party(address=address)]}))

        result = await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert result is not None
        assert result.legal_address == address

    @pytest.mark.unit
    async def test_missing_address_is_none(self):
        gateway, _ = make_gateway(json_response({"suggestions": [party()]}))

        result = await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert result is not None
        assert result.legal_address is None

    @pytest.mark.unit
    @pytest.mark.parametrize(
        ("dadata_type", "kind"),
        [
            ("LEGAL", Kind.COMPANY),
            ("BRANCH", Kind.COMPANY),
            ("FOREIGN_BRANCH", Kind.COMPANY),
            ("INDIVIDUAL", Kind.INDIVIDUAL),
            ("INDIVIDUAL_JOINT_VENTURE", Kind.INDIVIDUAL),
        ],
    )
    async def test_maps_type_to_kind(self, dadata_type, kind):
        gateway, _ = make_gateway(json_response({"suggestions": [party(type_=dadata_type)]}))

        result = await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert result.kind == kind

    @pytest.mark.unit
    @pytest.mark.parametrize("status", ["INACTIVE", "LIQUIDATING", "LIQUIDATED", "SUSPENDED"])
    async def test_non_active_status_is_inactive(self, status):
        gateway, _ = make_gateway(json_response({"suggestions": [party(status=status)]}))

        result = await gateway.fetch(Kind.COMPANY, TAX_ID)

        assert result.is_active is False

    @pytest.mark.unit
    async def test_returns_none_for_empty_suggestions(self):
        gateway, _ = make_gateway(json_response({"suggestions": []}))

        assert await gateway.fetch(Kind.COMPANY, TAX_ID) is None

    @pytest.mark.unit
    async def test_returns_none_when_no_suggestion_matches_exact_bin(self):
        gateway, _ = make_gateway(json_response({"suggestions": [party(bin_="999999999999")]}))

        assert await gateway.fetch(Kind.COMPANY, TAX_ID) is None

    @pytest.mark.unit
    @pytest.mark.parametrize("status_code", [401, 403, 429, 500, 503])
    async def test_http_error_means_unavailable(self, status_code):
        gateway, _ = make_gateway(json_response({"message": "error"}, status_code=status_code))

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    async def test_network_error_means_unavailable(self):
        def handler(request):
            raise httpx.ConnectTimeout("timeout", request=request)

        gateway, _ = make_gateway(handler)

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    async def test_unknown_response_shape_means_unavailable(self):
        gateway, _ = make_gateway(json_response({"unexpected": True}))

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)

    @pytest.mark.unit
    async def test_unknown_type_means_unavailable(self):
        gateway, _ = make_gateway(json_response({"suggestions": [party(type_="SOMETHING_NEW")]}))

        with pytest.raises(TaxpayerRegistryUnavailableError):
            await gateway.fetch(Kind.COMPANY, TAX_ID)
