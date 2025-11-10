import pytest

from src.app.services.geodata.service import GeodataService


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
    geodata_repository, geodata_client, config, exp_location_name, lat, lon
):
    geodata_service = GeodataService(geodata_repository, config, geodata_client)
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
            40.71273945,
            -74.00593904130275,
        ),
        (
            "Fleming Way, London Borough of Bexley,"
            + " London, Greater London, England, SE28 8NS, United Kingdom",
            51.5073599,
            0.1283349,
        ),
    ],
)
async def test_get_location_data_from_location_name(
    geodata_repository, geodata_client, config, location_name, exp_lat, exp_lon
):
    geodata_service = GeodataService(geodata_repository, config, geodata_client)
    res = await geodata_service.get_location_data_from_location_name(
        query=location_name,
    )

    assert res.display_name == location_name
    assert res.lat == exp_lat
    assert res.lon == exp_lon
