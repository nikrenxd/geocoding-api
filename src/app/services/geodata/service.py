import logging

from src.app.core.config import Settings
from src.app.models.geodata import Geodata
from src.app.repositories.geodata import GeodataRepository
from src.app.services.geodata.client import GeodataClient

logger = logging.getLogger("services.geodata.service")


class GeodataService:
    def __init__(
        self,
        repository: GeodataRepository,
        config: Settings,
        client: GeodataClient,
    ):
        self.repository = repository
        self.client = client
        self.config = config

    def _convert_json_data(self, data: dict) -> dict:
        dict_keys = ("display_name", "lat", "lon")
        dict_copy = data.copy()

        new_data = {key: dict_copy[key] for key in dict_keys}
        new_data["lat"] = float(new_data["lat"])
        new_data["lon"] = float(new_data["lon"])

        return new_data

    async def get_location_data_from_location_name(self, query: str) -> Geodata | None:
        response_data = await self.client.request_data_from_api(True, q=query)
        if not response_data:
            return None

        data = self._convert_json_data(response_data)
        return await self.repository.save_data(data)

    async def get_location_data_from_coords(
        self, lat: float, lon: float
    ) -> Geodata | None:
        response_data = await self.client.request_data_from_api(False, lat=lat, lon=lon)
        if not response_data:
            return None

        data = self._convert_json_data(response_data)
        return await self.repository.save_data(data)

    async def get_location_data_by_current_date(self) -> list[Geodata] | None:
        return await self.repository.get_data_by_current_date()

    async def delete_location_data_by_current_date(self) -> None:
        await self.repository.delete_current_date_data()
