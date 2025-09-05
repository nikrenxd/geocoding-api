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

    def _validate_data_list(self, data: list[dict]) -> list[dict]:
        return [self._convert_json_data(d) for d in data]

    def _validate_data(self, data: dict) -> dict:
        return self._convert_json_data(data)

    async def _request_data_from_api(
        self, many: bool, **url_params
    ) -> list[dict] | dict:
        async with AsyncClient() as client:
            api_url = (
                self.config.EXTERNAL_API_URL
                if many
                else self.config.EXTERNAL_COORD_API_URL
            )
            response = await client.get(
                url=api_url,
                params={**url_params, "api_key": self.config.API_KEY},
            )
        response_data = response.json()
        if many:
            return self._validate_data_list(response_data)
        return self._validate_data(response_data)

    async def get_all_data(self) -> list[Geodata]:
        return await self.repository.get_all()

    async def get_location_data_from_location_name(
        self, **url_params
    ) -> list[Geodata] | Geodata | None:
        response = await self._request_data_from_api(True, **url_params)
        if len(response) == 0:
            return None
        return await self.repository.save_data_list(response)

    async def get_location_data_from_coords(self, **url_params) -> Geodata | None:
        response = await self._request_data_from_api(False, **url_params)
        if not response:
            return None
        return await self.repository.save_data(response)
