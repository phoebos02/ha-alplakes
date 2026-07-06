import pytest

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResultType

from custom_components.alplakes.const import (
    DEFAULT_DEPTH,
    DEFAULT_LAKE,
    DEFAULT_LATITUDE,
    DEFAULT_LOCATION_NAME,
    DEFAULT_LONGITUDE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from custom_components.alplakes.helpers import make_measurement_id, sanitize_location_name


USER_INPUT = {
    "lake": DEFAULT_LAKE,
    "location_name": DEFAULT_LOCATION_NAME,
    "latitude": DEFAULT_LATITUDE,
    "longitude": DEFAULT_LONGITUDE,
    "depth": DEFAULT_DEPTH,
    "scan_interval": DEFAULT_SCAN_INTERVAL,
}


async def _start_user_flow(hass):
    return await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )


async def _configure_user_flow(hass, user_input):
    result = await _start_user_flow(hass)
    return await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input,
    )


@pytest.mark.asyncio
async def test_flow_shows_form_with_defaults(hass):
    """Test that the initial config flow shows a form with defaults."""
    result = await _start_user_flow(hass)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


@pytest.mark.asyncio
async def test_flow_user_success(hass):
    """Test completing the user config flow."""
    result = await _configure_user_flow(hass, USER_INPUT)

    assert result["type"] is FlowResultType.CREATE_ENTRY
    expected_title = (
        f"Lake {DEFAULT_LAKE.capitalize()} - "
        f"{sanitize_location_name(DEFAULT_LOCATION_NAME).capitalize()} "
        f"({DEFAULT_LATITUDE}, {DEFAULT_LONGITUDE})"
    )
    assert result["title"] == expected_title
    assert result["data"] == {**USER_INPUT, "location_name": sanitize_location_name(DEFAULT_LOCATION_NAME)}


@pytest.mark.asyncio
async def test_flow_sets_measurement_point_unique_id(hass):
    """Test that the flow unique ID includes the full measurement point."""
    result = await _configure_user_flow(hass, USER_INPUT)

    expected_unique_id = make_measurement_id(
        DEFAULT_LAKE,
        DEFAULT_LOCATION_NAME,
        DEFAULT_LATITUDE,
        DEFAULT_LONGITUDE,
        DEFAULT_DEPTH,
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == expected_unique_id


@pytest.mark.asyncio
async def test_flow_duplicate_same_measurement_point(hass):
    """Test that identical measurement points abort as already configured."""
    first_result = await _configure_user_flow(hass, USER_INPUT)
    second_result = await _configure_user_flow(hass, USER_INPUT)

    assert first_result["type"] is FlowResultType.CREATE_ENTRY
    assert second_result["type"] is FlowResultType.ABORT
    assert second_result["reason"] == "already_configured"


@pytest.mark.asyncio
async def test_flow_allows_same_location_with_different_coordinates(hass):
    """Test that the same label can be used for a different measurement point."""
    first_result = await _configure_user_flow(hass, USER_INPUT)
    second_result = await _configure_user_flow(
        hass,
        {
            **USER_INPUT,
            "latitude": DEFAULT_LATITUDE + 0.01,
        },
    )

    assert first_result["type"] is FlowResultType.CREATE_ENTRY
    assert second_result["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("latitude", 91),
        ("latitude", -91),
        ("longitude", 181),
        ("longitude", -181),
        ("depth", -0.1),
    ],
)
async def test_flow_rejects_invalid_measurement_values(hass, field, value):
    """Test that invalid coordinates and depths are rejected by the form."""
    result = await _start_user_flow(hass)
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            **USER_INPUT,
            field: value,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert field in result["errors"]
