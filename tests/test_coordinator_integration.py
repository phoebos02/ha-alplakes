# tests/test_coordinator_integration.py

import pytest
from custom_components.alplakes.coordinator import LakeDataCoordinator

@pytest.mark.enable_socket
@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_alplakes_fetch(hass, socket_enabled):
    """Live integration test against alplakes.eawag.ch API."""
    # Zürichsee station location
    lat = 47.25686
    lon = 8.69893
    depth = 0.35

    coord = LakeDataCoordinator(
        hass=hass,
        lake="zurich",
        latitude=lat,
        longitude=lon,
        depth=depth,
        scan_interval=30,
        location_name="IntegrationTestLocation"
    )

    temperature = await coord._async_update_data()

    assert isinstance(temperature, float)
    assert 0 <= temperature <= 40  # sanity check for water temp
    print(f"🌡️ Live temperature fetched: {temperature} °C")
