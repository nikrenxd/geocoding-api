from dataclasses import asdict, dataclass, fields
from typing import Self

from httpx import AsyncClient

from src.app.core.config import Settings
from src.app.repositories import GeodataRepository


@dataclass(frozen=True)
class GeodataModel:
    display_name: str
    lat: float
    lon: float

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(*[data.get(field.name) for field in fields(cls)])


class GeodataService:
    def __init__(self, repository: GeodataRepository, config: Settings):
        self.repository = repository
        self.config = config

    @staticmethod
    def _validate_data(data: list[dict]) -> list[dict]:
        return [asdict(GeodataModel.from_dict(d)) for d in data]

    async def _request_data_from_api(self, **url_params) -> list[dict]:
        async with AsyncClient() as client:
            response = await client.get(
                url=self.config.EXTERNAL_API_URL,
                params={**url_params},
            )
        validated_data = self._validate_data(response.json())
        return validated_data

    async def get_all_data(self) -> list[GeodataModel]:
        return await self.repository.get_all()

    async def convert_location_to_coords(
        self, location: str
    ) -> list[GeodataModel] | None:
        response = await self._request_data_from_api(
            q=location,
            api_key=self.config.API_KEY,
        )
        return await self.repository.save_data(response)

    async def convert_coords_to_location(
        self, lat: float, lon: float
    ) -> list[GeodataModel] | None:
        response = await self._request_data_from_api(
            lat=lat,
            lon=lon,
            api_key=self.config.API_KEY,
        )
        return await self.repository.save_data(response)
