import pytest

from src.app.services import GeodataService


@pytest.mark.anyio
@pytest.mark.parametrize(
    "exp_location_name,lat,lon",
    [
        (
            "New York City Hall, 260, Broadway,"
            + " Lower Manhattan, Manhattan Community Board 1,"
            + " Manhattan, New York County, New York, 10000, United States",
            40.7127,
            -74.0059,
        ),
        (
            "Fleming Way, London Borough of Bexley,"
            + " London, Greater London, England, SE28 8NS, United Kingdom",
            51.5074,
            0.1283,
        ),
    ],
)
async def test_get_location_data_from_coords(
    geodata_repository, config, exp_location_name, lat, lon
):
    geodata_service = GeodataService(geodata_repository, config)
    res = await geodata_service.get_location_data_from_coords(lat=lat, lon=lon)

    assert res.display_name == exp_location_name


@pytest.mark.anyio
@pytest.mark.parametrize(
    "location_name,exp_lat,exp_lon",
    [
        (
            "New York City Hall, 260, Broadway,"
            + " Lower Manhattan, Manhattan Community Board 1,"
            + " Manhattan, New York County, New York, 10000, United States",
            40.7127,
            -74.0059,
        ),
        (
            "Fleming Way, London Borough of Bexley,"
            + " London, Greater London, England, SE28 8NS, United Kingdom",
            51.5074,
            0.1283,
        ),
    ],
)
async def test_get_location_data_from_location_name(
    geodata_repository, config, location_name, exp_lat, exp_lon
):
    geodata_service = GeodataService(geodata_repository, config)
    res = await geodata_service.get_location_data_from_location_name(
        q=location_name
    )

    assert len(res) != 0
    assert res[0].display_name == location_name
    assert round(res[0].lat, 4) == exp_lat
    assert round(res[0].lon, 4) == exp_lon
