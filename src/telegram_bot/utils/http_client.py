import logging
import sys
from enum import Enum
from json import JSONDecodeError
from typing import Any, Tuple, Type
from urllib.parse import urljoin

import httpx


def get_logger(level: str = logging.DEBUG):
    _logger = logging.getLogger("solution_logger")
    _logger.setLevel(level)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(
        logging.Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s")
    )
    _logger.addHandler(handler)
    return _logger


logger = get_logger()


class HTTPClient:
    def __init__(self, base_url: str):
        self._base_url = base_url

    async def get(self, endpoint_path: str, **request_params) -> Any:
        return await self._request("GET", endpoint_path, **request_params)

    async def post(self, endpoint_path: str, **request_params) -> Any:
        return await self._request("POST", endpoint_path, **request_params)

    async def put(self, endpoint_path: str, **request_params) -> Any:
        return await self._request("PUT", endpoint_path, **request_params)

    async def patch(self, endpoint_path: str, **request_params) -> Any:
        return await self._request("PATCH", endpoint_path, **request_params)

    async def delete(self, endpoint_path: str, **request_params) -> Any:
        return await self._request("DELETE", endpoint_path, **request_params)

    async def _request(
        self, method: str, endpoint_path: str, **request_params: dict
    ) -> tuple[str | Any, Type[Enum] | Any]:
        url: str = urljoin(self._base_url, endpoint_path)
        logger.debug(f"Request: {method} {endpoint_path}")
        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.request(
                method, url, **request_params
            )
            try:
                content = response.json()
            except JSONDecodeError:
                content = response.text
            logger.debug(
                f"Response: {content} Code: {httpx.codes(response.status_code)} "
            )
            return content, httpx.codes(response.status_code)
