from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .sensor import async_setup_entry as setup_sensor_entry

DOMAIN = "alplakes"

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await setup_sensor_entry(hass, entry)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True
