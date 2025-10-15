import logging

import httpx
from httpx import AsyncClient

from src.app.core.config import Settings

logger = logging.getLogger("services.geodata.client")


class GeodataClient:
    def __init__(self, config: Settings):
        self._config = config

    async def request_data_from_api(self, from_name: bool, **url_params) -> dict | None:
        async with AsyncClient() as client:
            try:
                api_url = (
                    self._config.EXTERNAL_API_URL
                    if from_name
                    else self._config.EXTERNAL_COORD_API_URL
                )
                response = await client.get(
                    url=api_url,
                    params={**url_params, "api_key": self._config.API_KEY},
                )

                response_data = response.json()
                if from_name:
                    return response_data[0]
                return response_data
            except httpx.TimeoutException:
                logger.error("Request timed out")
            except httpx.RequestError:
                logger.error("Failed to send request")
