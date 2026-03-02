from abc import abstractmethod
from http import HTTPMethod
from typing import Any, NewType, Protocol
from urllib.parse import ParseResult, urlparse

from httpx import AsyncClient

Headers = NewType("Headers", dict[str, Any])
Url = NewType("Url", ParseResult)


class HTTPClient(Protocol):
    @abstractmethod
    async def request(
        self,
        method: HTTPMethod,
        path: str,
        params: dict[str, str],
        data: dict[str, Any] | None = None,
    ) -> Any:
        raise NotImplementedError


class HTTPXClient(HTTPClient):
    def __init__(self, base_url: Url, headers: Headers | None = None, timeout: int = 5):
        self._url = base_url
        self._headers = headers
        self._timeout = timeout

    async def request(
        self,
        method: HTTPMethod,
        path: str,
        params: dict[str, str],
        data: dict[str, Any] | None = None,
    ) -> Any:
        full_url = urlparse(url=f"{self._url}/{path}")
        async with AsyncClient(
            base_url=str(self._url), headers=self._headers
        ) as client:
            request = client.build_request(
                method=method,
                url=str(full_url),
                data=data,
                params=params,
                timeout=self._timeout,
            )
            resp = await client.send(request=request)
            resp.raise_for_status()

        return resp.json()
