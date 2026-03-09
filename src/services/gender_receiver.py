from http import HTTPMethod
from typing import Protocol, cast
from warnings import deprecated

from pydantic_ai import Agent

from src.infrastructure.http_client import HTTPClient
from src.models.types import Gender
from src.schemas.genderize import GenderizeResponse


class GenderReceiver(Protocol):
    async def get_gender_by_name(self, name: str) -> Gender:
        raise NotImplementedError


class GenderReceiverAI:
    def __init__(self, agent: Agent[str, str]):
        self._agent = agent

    async def get_gender_by_name(self, name: str) -> Gender:
        # TODO add redis for caching by name
        res = await self._agent.run(f"Give me gender: {name}")
        return cast(Gender, res.output)


@deprecated(
    "`GenderReceiverAPIGenderiz` is deprecated, use `GenderReceiverAI` instead."
)
class GenderReceiverAPIGenderize:
    def __init__(self, http_client: HTTPClient, country_id: str = "US"):
        self._client = http_client
        self._country_id = country_id

    async def get_gender_by_name(self, name: str) -> Gender:
        resp = await self._client.request(
            method=HTTPMethod.GET,
            path="",
            params={
                "name": name,
                "country_id": self._country_id,
            },
        )
        result = GenderizeResponse.model_validate(resp)
        if result.probability > 95:
            return Gender(result.gender)
        else:
            return Gender.unknown
