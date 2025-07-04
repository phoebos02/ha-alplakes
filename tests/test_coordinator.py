# tests/test_coordinator.py
import pytest
from datetime import datetime, timedelta, UTC
from unittest.mock import patch, AsyncMock, MagicMock
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.alplakes.coordinator import (
    LakeDataCoordinator, MODEL
)

@pytest.mark.enable_socket
@pytest.mark.asyncio
@pytest.mark.allow_hosts(['127.0.0.1', '152.88.10.20'])
async def test_successful_fetch(hass):
    """Coordinator should return rounded temperature on valid JSON."""
    hass = await anext(hass)  # Get the next value from the async generator
    now = datetime.now(UTC)
    start = now.strftime("%Y%m%d%H%M")
    end = (now + timedelta(hours=1)).strftime("%Y%m%d%H%M")
    expected_path = (
        f"/simulations/point/{MODEL}/zurich/"
        f"{start}/{end}/0.35/47.25/8.69"
    )
    expected_url = f"https://alplakes-api.eawag.ch{expected_path}?variables=temperature"

    # Mock response
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={
        "variables": {
            "temperature": {
                "data": [19.793],
                "unit": "degC"
            }
        }
    })

    # Create a mock session that returns our mock response
    mock_session = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock()

    # Patch ClientSession.get to return our mock session
    with patch("aiohttp.ClientSession.get", return_value=mock_session) as mock_get:
        coord = LakeDataCoordinator(
            hass=hass,
            lake="zurich",
            latitude=47.25,
            longitude=8.69,
            depth=0.35,
            scan_interval=30,
            location_name="UnitTestLocation"
        )
        temp = await coord._async_update_data()
        assert isinstance(temp, float)
        assert temp == round(19.793, 1)  # 19.8
        mock_get.assert_called_with(expected_url, timeout=10)

@pytest.mark.enable_socket
@pytest.mark.asyncio
@pytest.mark.allow_hosts(['127.0.0.1', '152.88.10.20'])
async def test_http_error_raises_update_failed(hass):
    """Coordinator should wrap non-200 into UpdateFailed."""
    hass = await anext(hass)  # Get the next value from the async generator
    # Mock response with status 500
    mock_response = MagicMock()
    mock_response.status = 500
    mock_response.json = AsyncMock(return_value={})

    # Create a mock session that returns our mock response
    mock_session = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock()

    with patch("aiohttp.ClientSession.get", return_value=mock_session):
        coord = LakeDataCoordinator(
            hass=hass,
            lake="zurich",
            latitude=0, longitude=0, depth=0,
            scan_interval=30,
            location_name="UnitTestLocation"
        )
        with pytest.raises(UpdateFailed, match="HTTP 500 from API"):
            await coord._async_update_data()
