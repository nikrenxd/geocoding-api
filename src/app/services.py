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
    def _validate_data_list(data: list[dict]) -> list[dict]:
        return [asdict(GeodataModel.from_dict(d)) for d in data]

    @staticmethod
    def _validate_data(data: dict) -> dict:
        return asdict(GeodataModel.from_dict(data))

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

    async def get_all_data(self) -> list[GeodataModel]:
        return await self.repository.get_all()

    async def get_location_data_from_location_name(
        self, **url_params
    ) -> list[GeodataModel] | GeodataModel | None:
        response = await self._request_data_from_api(True, **url_params)
        if len(response) == 0:
            return None
        return await self.repository.save_data_list(response)

    async def get_location_data_from_coords(
        self, **url_params
    ) -> GeodataModel | None:
        response = await self._request_data_from_api(False, **url_params)
        if not response:
            return None
        return await self.repository.save_data(response)
