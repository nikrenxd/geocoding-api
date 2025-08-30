import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories import GeodataRepository


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


@pytest.mark.anyio
@pytest.mark.parametrize(
    "data,expected",
    [
        (
            [
                {"display_name": "test1", "lat": 51.6, "lon": -0.1},
                {"display_name": "test2", "lat": 102.1, "lon": -0.2579},
                {"display_name": "test3", "lat": 59.9123, "lon": -0.1223},
            ],
            [
                "test1",
                "test2",
                "test3",
            ],
        ),
    ],
)
async def test_save_data_list(
    async_session: AsyncSession, data: list[dict], expected: list[str]
):
    geodata_repo = GeodataRepository(session=async_session)
    res = await geodata_repo.save_data_list(data)

    assert len(res) == len(expected)
    assert all(
        [
            geodata.display_name == ex
            for geodata, ex in zip(res, expected, strict=False)
        ]
    )
