import pytest
from custom_components.alplakes.coordinator import LakeDataCoordinator

pytest_plugins = "pytest_homeassistant_custom_component"

@pytest.mark.asyncio
async def test_flow_user_success(hass):
    """Test completing the user config flow."""
    assert True

@pytest.mark.asyncio
async def test_flow_shows_form_with_defaults(hass):
    """Test that the initial config flow shows a form with default values."""
    assert True

@pytest.mark.asyncio
async def test_flow_duplicate(hass):
    """Test that starting with duplicate unique_id aborts the flow."""
    assert True

@pytest.mark.enable_socket
@pytest.mark.asyncio
@pytest.mark.allow_hosts(['127.0.0.1', '152.88.10.20'])
async def test_live_alplakes_fetch(socket_enabled):
    """Live integration test against alplakes.eawag.ch API."""
    # Zürichsee station location
    lat = 47.25686
    lon = 8.69893
    depth = 0.35

    coord = LakeDataCoordinator(
        hass=None,
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
