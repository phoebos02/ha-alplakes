# tests/test_coordinator.py
import asyncio
import pytest
from datetime import datetime, timedelta
from aresponses import ResponsesMockServer
from aiohttp import ClientSession
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.alplakes_temperature.coordinator import (
    LakeDataCoordinator, BASE_URL, MODEL
)

@pytest.fixture
async def hass_loop(event_loop):
    return event_loop

@pytest.mark.asyncio
async def test_successful_fetch(hass_loop):
    """Coordinator should return rounded temperature on valid JSON."""
    # 1. Set up an aresponses server
    async with ResponsesMockServer(loop=hass_loop) as server:
        now = datetime.utcnow()
        start = now.strftime("%Y%m%d%H%M")
        end = (now + timedelta(hours=1)).strftime("%Y%m%d%H%M")
        path = (
            f"/simulations/point/{MODEL}/zurich/"
            f"{start}/{end}/0.35/47.25/8.69"
        )
        server.add(
            "alplakes-api.eawag.ch", 
            path + "?variables=temperature",
            "GET",
            aresponses.Response(
                status=200,
                headers={"Content-Type": "application/json"},
                text="""
                {
                  "variables": {
                    "temperature": {
                      "data": [19.793],
                      "unit": "degC"
                    }
                  }
                }
                """,
            ),
        )

        # 2. Point coordinator at our mock server
        coord = LakeDataCoordinator(
            hass=None,             # not used in _async_update_data
            lake="zurich",
            latitude=47.25,
            longitude=8.69,
            depth=0.35,
            scan_interval=30
        )
        # override the base URL to hit our mock
        coord.session = ClientSession()
        coord.BASE_URL = f"http://localhost:{server.port}/simulations/point"
        coord.MODEL = MODEL

        # 3. Invoke the fetch
        temp = await coord._async_update_data()
        # 4. Assert it rounds to one decimal
        assert isinstance(temp, float)
        assert temp == round(19.793, 1)  # 19.8

        await coord.session.close()

@pytest.mark.asyncio
async def test_http_error_raises_update_failed():
    """Coordinator should wrap non-200 into UpdateFailed."""
    # Simulate a 500 response without mocking body
    class DummyResp:
        status = 500
        async def json(self): return {}

    class DummySession:
        async def get(self, *args, **kwargs): return DummyResp()

    coord = LakeDataCoordinator(
        hass=None,
        lake="zurich",
        latitude=0, longitude=0, depth=0,
        scan_interval=30
    )
    coord.session = DummySession()

    with pytest.raises(UpdateFailed):
        await coord._async_update_data()
