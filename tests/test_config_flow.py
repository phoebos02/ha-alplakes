import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry
from custom_components.alplakes.const import DOMAIN, DEFAULT_LOCATION_NAME, DEFAULT_LAKE, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_DEPTH, DEFAULT_SCAN_INTERVAL

@pytest.mark.asyncio
async def test_flow_user_success(hass):
    """Test completing the user config flow."""
    # Start the flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    assert result["type"] == "form"
    assert result["step_id"] == "user"

    # Provide valid user input
    user_input = {
        "lake": "zurich",
        "location_name": DEFAULT_LOCATION_NAME,
        "latitude": 47.36,
        "longitude": 8.54,
        "depth": 1.0,
        "scan_interval": 30,
    }
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=user_input
    )
    # Verify that an entry was created
    assert result2["type"] == "create_entry"
    assert result2["title"].lower().startswith("zurich")
    assert result2["data"] == user_input

@pytest.mark.asyncio
async def test_flow_shows_form_with_defaults(hass):
    """Test that the initial config flow shows a form with default values."""
    # Trigger the initial user step
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )

    assert result["type"] == "form"
    assert result["step_id"] == "user"

    # The schema should include our six required fields
    data_schema = result["data_schema"]
    keys = {field.schema._schema.key
            for field in data_schema.schema}
    expected = {"lake", "location_name", "latitude", "longitude", "depth", "scan_interval"}
    assert expected <= keys

    # Defaults should be present in the schema for each field
    # Here we inspect default values in the voluptuous schema
    defaults = {
        field.schema._schema.key: field.schema._schema.default
        for field in data_schema.schema
        if hasattr(field.schema._schema, "default")
    }
    assert defaults.get("lake") == DEFAULT_LAKE
    assert defaults.get("location_name") == DEFAULT_LOCATION_NAME
    assert defaults.get("latitude") == DEFAULT_LATITUDE
    assert defaults.get("longitude") == DEFAULT_LONGITUDE
    assert defaults.get("depth") == DEFAULT_DEPTH
    assert defaults.get("scan_interval") == DEFAULT_SCAN_INTERVAL

@pytest.mark.asyncio
async def test_flow_duplicate(hass):
    """Test that starting with duplicate unique_id aborts the flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="lake_zurich_männedorf",
        data={
            "lake": "zurich",
            "location_name": DEFAULT_LOCATION_NAME,
            "latitude": 47.36,
            "longitude": 8.54,
            "depth": 1.0,
            "scan_interval": 30,
        },
    )
    entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "user"}
    )
    # Provide the same input → should be aborted
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input=entry.data,
    )
    assert result2["type"] == "abort"
    assert result2["reason"] == "already_configured"
