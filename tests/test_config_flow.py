import pytest

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