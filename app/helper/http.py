from typing import Any

import aiohttp

timeout = aiohttp.ClientTimeout(total=20)


class Http:
    @staticmethod
    async def get(
        url: str,
        params: dict[str, Any] = None,
        base_url: str = None,
        headers: dict[str, Any] = None,
    ) -> dict[str, Any]:
        if not params:
            params = {}
        async with aiohttp.ClientSession(
            base_url=base_url, headers=headers, timeout=timeout
        ) as session:
            async with session.get(url=url, params=params) as response:
                try:
                    response_json = await response.json()
                except aiohttp.ContentTypeError:
                    response_json = await response.text()
                status_code = response.status
        return status_code, response_json

    @staticmethod
    async def post(
        url: str,
        json: dict = None,
        data: dict = None,
        params: dict = None,
        base_url: str = None,
        headers: dict[str, Any] = None,
    ) -> dict[str, Any]:
        if data:
            post_input = {"url": url, "data": data}
        else:
            post_input = {"url": url, "json": json or {}}
        if params:
            post_input.update(params=params)
        async with aiohttp.ClientSession(
            base_url=base_url, headers=headers, timeout=timeout
        ) as session:
            async with session.post(**post_input) as response:
                try:
                    response_json = await response.json()
                except aiohttp.ContentTypeError:
                    response_json = await response.text()
                status_code = response.status
        return status_code, response_json
