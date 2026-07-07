import json
from datetime import datetime
from unittest.mock import patch

import pytest

from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.alplakes.const import BASE_URL, ONE_D_BASE_URL
from custom_components.alplakes.coordinator import LakeDataCoordinator


class FakeResponse:
    def __init__(self, body, status=200):
        self.body = body
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def text(self):
        return self.body


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.requested_url = None
        self.requested_timeout = None

    def get(self, url, timeout):
        self.requested_url = url
        self.requested_timeout = timeout
        return self.response


class FixedDateTime:
    @classmethod
    def now(cls, tz):
        return datetime(2026, 5, 30, 12, 0, tzinfo=tz)


def _make_coordinator(hass, lake="zurich", **kwargs):
    defaults = {
        "latitude": 47.25686,
        "longitude": 8.69893,
        "depth": 0.35,
        "scan_interval": 30,
        "location_name": "IntegrationTestLocation",
    }
    defaults.update(kwargs)
    return LakeDataCoordinator(hass, lake=lake, **defaults)


async def _update_with_body(coordinator, body, status=200):
    session = FakeSession(FakeResponse(body, status=status))
    coordinator.session = session

    with patch("custom_components.alplakes.coordinator.datetime", FixedDateTime):
        result = await coordinator._async_update_data()

    return result, session

@pytest.mark.asyncio
async def test_coordinator_maps_lake_to_api_lake_and_model(hass):
    """Test API lake aliases and model selection."""
    brunnen = _make_coordinator(hass, lake="brunnen")
    zurich = _make_coordinator(hass, lake="zurich")
    thun = _make_coordinator(hass, lake="thun")
    neuchatel = _make_coordinator(hass, lake="neuchatel")
    pfaffikersee = _make_coordinator(hass, lake="pfaffikersee")
    wolfgangsee = _make_coordinator(hass, lake="wolfgangsee")
    aegeri = _make_coordinator(hass, lake="aegeri")

    assert brunnen.api_lake == "lucerne"
    assert brunnen.model == "mitgcm"
    assert brunnen.is_1d is False
    assert zurich.api_lake == "zurich"
    assert zurich.model == "delft3d-flow"
    assert zurich.is_1d is False
    assert thun.model == "simstrat"
    assert thun.is_1d is True
    assert neuchatel.model == "mitgcm"
    assert neuchatel.is_1d is False
    assert pfaffikersee.api_lake == "pfaffikon"
    assert pfaffikersee.model == "simstrat"
    assert pfaffikersee.is_1d is True
    assert wolfgangsee.model == "simstrat"
    assert wolfgangsee.is_1d is True
    assert aegeri.api_lake == "ageri"
    assert aegeri.model == "delft3d-flow"
    assert aegeri.is_1d is False


@pytest.mark.asyncio
async def test_coordinator_builds_url_with_api_lake_and_model(hass):
    """Test URL construction uses translated API lake and selected model."""
    coordinator = _make_coordinator(hass, lake="brunnen", depth=0.1)
    body = json.dumps({"variables": {"temperature": {"data": [10.0, 12.34]}}})

    result, session = await _update_with_body(coordinator, body)

    assert result == 12.3
    assert session.requested_timeout == 10
    assert session.requested_url == (
        f"{BASE_URL}/mitgcm/lucerne/202605300800/202605301200/"
        "0.1/47.25686/8.69893?variables=temperature"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("lake", "api_lake"),
    [
        ("pfaffikersee", "pfaffikon"),
        ("wolfgangsee", "wolfgangsee"),
    ],
)
async def test_coordinator_builds_1d_url_for_non_3d_lakes(hass, lake, api_lake):
    """Test 1d Simstrat lakes use the 1d point API without coordinates."""
    coordinator = _make_coordinator(hass, lake=lake, depth=1)
    body = json.dumps({"variables": {"T": {"data": [10.0, 12.34]}}})

    result, session = await _update_with_body(coordinator, body)

    assert result == 12.3
    assert session.requested_timeout == 10
    assert session.requested_url == (
        f"{ONE_D_BASE_URL}/simstrat/{api_lake}/202605300800/202605301200/"
        "1?variables=T"
    )


@pytest.mark.asyncio
async def test_coordinator_uses_3d_when_lake_exists_in_both_apis(hass):
    """Test a lake present in both metadata sets keeps the 3d endpoint."""
    coordinator = _make_coordinator(hass, lake="biel", depth=0.1)
    body = json.dumps({"variables": {"temperature": {"data": [10.0, 12.34]}}})

    result, session = await _update_with_body(coordinator, body)

    assert result == 12.3
    assert coordinator.is_1d is False
    assert session.requested_url == (
        f"{BASE_URL}/delft3d-flow/biel/202605300800/202605301200/"
        "0.1/47.25686/8.69893?variables=temperature"
    )


@pytest.mark.asyncio
async def test_coordinator_parses_temperature_and_rounds(hass):
    """Test successful temperature parsing and rounding."""
    coordinator = _make_coordinator(hass)
    body = json.dumps({"variables": {"temperature": {"data": [10.0, 12.34]}}})

    result, _session = await _update_with_body(coordinator, body)

    assert result == 12.3


@pytest.mark.asyncio
async def test_coordinator_raises_update_failed_for_http_error(hass):
    """Test non-200 responses are reported as update failures."""
    coordinator = _make_coordinator(hass)

    with pytest.raises(UpdateFailed, match="HTTP 500 from API"):
        await _update_with_body(coordinator, "server error", status=500)


@pytest.mark.asyncio
async def test_coordinator_raises_update_failed_for_invalid_json(hass):
    """Test invalid JSON is reported clearly."""
    coordinator = _make_coordinator(hass)

    with pytest.raises(UpdateFailed, match="Invalid JSON from API"):
        await _update_with_body(coordinator, "not json")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"variables": {}},
        {"variables": {"temperature": {}}},
    ],
)
async def test_coordinator_raises_update_failed_for_missing_temperature_data(
    hass, payload
):
    """Test missing expected API fields are wrapped as update failures."""
    coordinator = _make_coordinator(hass)

    with pytest.raises(UpdateFailed, match="Failed to fetch or parse data"):
        await _update_with_body(coordinator, json.dumps(payload))


@pytest.mark.asyncio
async def test_coordinator_raises_update_failed_for_empty_temperature_data(hass):
    """Test empty temperature data is reported clearly."""
    coordinator = _make_coordinator(hass)
    body = json.dumps({"variables": {"temperature": {"data": []}}})

    with pytest.raises(UpdateFailed, match="No temperature data returned from API"):
        await _update_with_body(coordinator, body)


@pytest.mark.asyncio
@pytest.mark.parametrize("value", ["not-a-number", None])
async def test_coordinator_raises_update_failed_for_non_numeric_temperature(
    hass, value
):
    """Test non-numeric temperature values are wrapped as update failures."""
    coordinator = _make_coordinator(hass)
    body = json.dumps({"variables": {"temperature": {"data": [value]}}})

    with pytest.raises(UpdateFailed, match="Failed to fetch or parse data"):
        await _update_with_body(coordinator, body)
