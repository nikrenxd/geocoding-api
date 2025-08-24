import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories import GeodataRepository


@pytest.mark.anyio
@pytest.mark.parametrize(
    "address,lat,lon",
    (
        ("Test1", 22.12, 23.11),
        ("Test2", 13.129, -111.9019),
        ("Test2", 58.12918, -127.9819),
    ),
)
async def test_save_data(
    async_session: AsyncSession, address: str, lat: float, lon: float
):
    geodata_repo = GeodataRepository(session=async_session)
    res = await geodata_repo.save_data(address=address, lat=lat, lon=lon)

    assert res == address
