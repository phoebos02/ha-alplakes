import pytest

from custom_components.alplakes.coordinator import LakeDataCoordinator


@pytest.mark.enable_socket
@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("lake", "lat", "lon", "depth"),
    [
        ("zurich", 47.25686, 8.69893, 0.35),
        ("pfaffikersee", 47.345, 8.785, 1),
        ("wolfgangsee", 47.745, 13.435, 1),
    ],
)
async def test_live_alplakes_fetch(hass, socket_enabled, lake, lat, lon, depth):
    """Live integration test against alplakes.eawag.ch API."""
    coord = LakeDataCoordinator(
        hass=hass,
        lake=lake,
        latitude=lat,
        longitude=lon,
        depth=depth,
        scan_interval=30,
        location_name="IntegrationTestLocation",
    )

    temperature = await coord._async_update_data()

    assert isinstance(temperature, float)
    assert 0 <= temperature <= 40
    print(f"Live temperature fetched for {lake}: {temperature} C")
