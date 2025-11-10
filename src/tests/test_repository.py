import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.geodata import GeodataRepository


@pytest.mark.anyio
@pytest.mark.parametrize(
    "data,expected",
    [
        (
            {"display_name": "test1", "lat": 51.6, "lon": -0.1},
            "test1",
        ),
        (
            {"display_name": "test2", "lat": 51.1, "lon": -0.2},
            "test2",
        ),
    ],
)
async def test_save_data(
    async_session: AsyncSession,
    data: dict,
    expected: str,
):
    geodata_repo = GeodataRepository(session=async_session)
    res = await geodata_repo.save_data(data)

    assert res.display_name == expected
