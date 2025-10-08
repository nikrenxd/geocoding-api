from httpx import AsyncClient

from src.app.core.config import Settings
from src.app.models import Geodata
from src.app.repositories import GeodataRepository


class GeodataService:
    def __init__(self, repository: GeodataRepository, config: Settings):
        self.repository = repository
        self.config = config

    @staticmethod
    def _convert_json_data(data: dict) -> dict:
        dict_keys = ("display_name", "lat", "lon")
        dict_copy = data.copy()

        new_data = {key: dict_copy[key] for key in dict_keys}
        new_data["lat"] = float(new_data["lat"])
        new_data["lon"] = float(new_data["lon"])

        return new_data

    def _validate_data(self, data: dict) -> dict:
        return self._convert_json_data(data)

    async def _request_data_from_api(
        self, from_name: bool, **url_params
    ) -> list[dict] | dict:
        async with AsyncClient() as client:
            api_url = (
                self.config.EXTERNAL_API_URL
                if from_name
                else self.config.EXTERNAL_COORD_API_URL
            )
            response = await client.get(
                url=api_url,
                params={**url_params, "api_key": self.config.API_KEY},
            )
        response_data = response.json()
        if from_name:
            return self._validate_data(response_data[0])
        return self._validate_data(response_data)

    async def get_location_data_from_location_name(
        self, query: str
    ) -> list[Geodata] | Geodata | None:
        response = await self._request_data_from_api(True, q=query)
        if not response:
            return None
        return await self.repository.save_data(response)

    async def get_location_data_from_coords(self, **url_params) -> Geodata | None:
        response = await self._request_data_from_api(False, **url_params)
        if not response:
            return None
        return await self.repository.save_data(response)
