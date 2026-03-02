from http import HTTPMethod

from src.infrastructure.http_client import HTTPClient
from src.schemas.genderize import GenderizeResponse


class Genderize:
    """
    Service for receive gender by name
    """

    def __init__(self, http_client: HTTPClient):
        self._client = http_client

    async def get_by_one_name(self, name: str, country_id: str = "US") -> GenderizeResponse:
        resp = await self._client.request(
            method=HTTPMethod.GET,
            path="",
            params={
                "name": name,
                "country_id": country_id,
            },
        )
        result = GenderizeResponse.model_validate(resp)
        return result
