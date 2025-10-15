from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from src.app.api.v1.schemas import (
    GeodataLocationResponse,
    GeodataResponse,
)
from src.app.services.geodata.service import GeodataService

router = APIRouter(prefix="/api/geocode", tags=["location"])


@router.get("/location")
@inject
async def from_location_to_coords(
    query_location: str, service: FromDishka[GeodataService]
) -> GeodataResponse:
    result = await service.get_location_data_from_location_name(query=query_location)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


@router.get("/coords")
@inject
async def from_coords_to_location(
    latitude: float, longitude: float, service: FromDishka[GeodataService]
) -> GeodataLocationResponse:
    result = await service.get_location_data_from_coords(lat=latitude, lon=longitude)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result
