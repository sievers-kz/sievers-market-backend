from typing import Optional

import httpx
from loguru import logger

from src.core.vendor.application.interfaces.taxpayer_gateway import ITaxpayerGateway
from src.core.vendor.domain.enums import LegalForm
from src.core.vendor.presentation.dto import TaxpayerResponse

KGD_TAXPAYER_TYPE_MAP = {
    LegalForm.IE: "IP",
    LegalForm.LLP: "UL",
    LegalForm.JSC: "UL",
    LegalForm.FARM: "IP",
}


class MockTaxpayerGateway(ITaxpayerGateway):
    def __init__(self):
        self._taxpayers_database = {
            "020716550967": {
                "name": "Индивидуальный предприниматель AGROW",
                "type": "IP",
                "is_liquidation": False,
            },
            "180240041089": {
                "name": "Товарищество с ограниченной ответственностью Olzha Agro",
                "type": "UL",
                "is_liquidation": False,
            },
            "050540005822": {
                "name": "Товарищество с ограниченной ответственностью Родина",
                "type": "UL",
                "is_liquidation": True,
            },
        }

    async def fetch(
        self, tax_id: str, legal_form: LegalForm = LegalForm.LLP
    ) -> Optional[TaxpayerResponse]:
        taxpayer = self._taxpayers_database.get(tax_id)
        if not taxpayer or taxpayer["type"] != KGD_TAXPAYER_TYPE_MAP[legal_form]:
            return None

        return TaxpayerResponse(
            tax_id=tax_id,
            legal_name=taxpayer["name"],
            legal_form=legal_form,
            is_liquidation=taxpayer["is_liquidation"],
        )


class KGDTaxpayerGateway(ITaxpayerGateway):
    TAXPAYER_URL = (
        "https://portal.kgd.gov.kz/services/isnaportalsync/public/taxpayer-data"
    )

    def __init__(self, portal_token: str):
        self._portal_token = portal_token

    async def fetch(
        self, tax_id: str, legal_form: LegalForm
    ) -> TaxpayerResponse | None:
        params = {
            "taxpayerCode": tax_id,
            "taxpayerType": KGD_TAXPAYER_TYPE_MAP[legal_form],
            "print": "false",
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    self.TAXPAYER_URL,
                    params=params,
                    headers={"X-Portal-Token": self._portal_token},
                )
                response.raise_for_status()
                data = response.json()

        except httpx.HTTPStatusError as exc:
            logger.error(
                "KGD HTTP error | status={} tax_id={}", exc.response.status_code, tax_id
            )
            return None
        except httpx.RequestError as exc:
            logger.error("KGD request error | tax_id={} error={}", tax_id, exc)
            return None

        responses = data.get("taxpayerPortalSearchResponses", [])
        if not responses:
            return None

        entry = responses[0]
        if entry.get("messageResult") != "SUCCESS":
            return None

        legal_name = entry.get("name")
        if not legal_name:
            return None

        is_liquidation = (
            entry.get("endDate") is not None or entry.get("endReason") is not None
        )

        return TaxpayerResponse(
            tax_id=entry["code"],
            legal_name=legal_name,
            legal_form=legal_form,
            is_liquidation=is_liquidation,
        )
