import pytest
from custom_components.alplakes.config_flow import AlplakesConfigFlow, VALID_LAKES, DEFAULT_LOCATION_NAME, DEFAULT_LAKE, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_DEPTH, DEFAULT_SCAN_INTERVAL

@pytest.mark.asyncio
async def test_show_user_form(hass):
    """Test that the user step shows the form with defaults when no input is provided."""
    flow = AlplakesConfigFlow()
    flow.hass = hass
    result = await flow.async_step_user()
    assert result["type"] == "form"
    schema = result["data_schema"]
    # Check that the schema has the expected defaults
    assert schema({})["lake"] == DEFAULT_LAKE
    assert schema({})["location_name"] == DEFAULT_LOCATION_NAME
    assert schema({})["latitude"] == DEFAULT_LATITUDE
    assert schema({})["longitude"] == DEFAULT_LONGITUDE
    assert schema({})["depth"] == DEFAULT_DEPTH
    assert schema({})["scan_interval"] == DEFAULT_SCAN_INTERVAL

@pytest.mark.asyncio
async def test_create_entry_from_user_input(hass):
    """Test that the user step creates an entry when valid input is provided."""
    flow = AlplakesConfigFlow()
    flow.hass = hass
    user_input = {
        "lake": VALID_LAKES[1],
        "location_name": "TestLocation",
        "latitude": 46.2,
        "longitude": 6.1,
        "depth": 2.5,
        "scan_interval": 15,
    }
    # Patch unique_id check to not abort
    flow._abort_if_unique_id_configured = lambda: None
    result = await flow.async_step_user(user_input)
    assert result["type"] == "create_entry"
    assert result["title"].startswith(f"Lake {user_input['lake']}")
    assert result["data"] == user_input
