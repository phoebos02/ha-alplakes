# tests/test_e2e.py

import os
import pytest
import requests

@pytest.mark.e2e
def test_end_to_end_sensor_state():
    """
    E2E: Fetch the sensor state from the running Home Assistant instance
    and verify the temperature is within a sane range (0–40 °C).
    """
    # Required environment variables
    host = os.getenv("HA_HOST")
    token = os.getenv("HA_TOKEN")
    entity_id = os.getenv("HA_ENTITY_ID")

    assert host, "HA_HOST must be set"
    assert token, "HA_TOKEN must be set"
    assert entity_id, "HA_ENTITY_ID must be set"

    url = f"http://{host}:8123/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    resp = requests.get(url, headers=headers, timeout=10)
    assert resp.status_code == 200, f"Unexpected status: {resp.status_code}"

    data = resp.json()
    # The 'state' field is a string; convert to float
    temperature = float(data.get("state", -999))
    assert 0.0 <= temperature <= 40.0, (
        f"Temperature {temperature}°C out of expected range"
    )
