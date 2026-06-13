import httpx


class SigexClient:
    def __init__(self):
        self.base_url = "https://test.sigex.kz"

    async def initialize_session(self, tax_id: str) -> dict:
        url = f"{self.base_url}/api/egovQr"
        payload = {
            "description": "Подтвердите свою личность на платформе AGROW",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()

            data = response.json()
            return data

    async def push_signing_data(self, data_url: str, tax_id: str) -> None:
        payload = {
            "signMethod": "CMS_SIGN_ONLY",
            "documentsToSign": [
                {
                    "id": 1,
                    "nameRu": "Подтверждение БИН компании в AGROW",
                    "nameKz": "AGROW жүйесінде БСН растау",
                    "nameEn": "AGROW Business Verification",
                    "meta": [{"name": "Проверяемый БИН/ИИН", "value": tax_id}],
                    "document": {"file": {"mime": "text/plain", "data": tax_id}},
                }
            ],
        }

        timeout = httpx.Timeout(120.0, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(data_url, json=payload)
            response.raise_for_status()

    async def fetch_signatures(self, sign_url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(sign_url)

            if response.status_code == 404:
                raise ValueError("QR-код еще не отсканирован в eGov Mobile")

            response.raise_for_status()
            data = response.json()

            try:
                signer_info = data["signers"]
                confirmed_tax_id = (
                    signer_info.get("bin")
                    or signer_info.get("egov")
                    or signer_info.get("iin")
                )
                if not confirmed_tax_id:
                    raise ValueError("Идентификатор отсутствует в ЭЦП")
                return confirmed_tax_id

            except (KeyError, IndexError):
                raise ValueError("Не удалось распарсить структуру подписи eGov")
