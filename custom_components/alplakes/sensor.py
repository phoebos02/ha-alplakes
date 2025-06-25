from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .coordinator import LakeDataCoordinator
from homeassistant.components.sensor import SensorEntity

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    data = entry.data
    lake, lat, lng, depth, interval = data["lake"], data["latitude"], data["longitude"], data["depth"], data["scan_interval"]

    coordinator = LakeDataCoordinator(hass, lake, lat, lng, depth, interval)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([LakeTemperatureSensor(coordinator, lake, lat, lng, depth)])

class LakeTemperatureSensor(SensorEntity):
    def __init__(self, coordinator, lake, lat, lng, depth):
        self.coordinator = coordinator
        self._attr_unique_id = f"alplakes_{lake}_{lat}_{lng}_{depth}"
        self._attr_name = f"{lake.capitalize()} Temperature ({depth} m)"
        self._attr_native_unit_of_measurement = "°C"
        self._attr_attribution = "Data provided by Alplakes / Eawag"

    @property
    def state(self):
        return self.coordinator.data

    @property
    def available(self):
        return self.coordinator.last_update_success

    @property
    def device_info(self):
        return {
            "identifiers": {("alplakes", self.unique_id)},
            "name": f"Alplakes – {self.coordinator.lake}",
            "manufacturer": "Eawag",
            "model": "Delft3D-Flow",
        }

    async def async_added_to_hass(self):
        self.coordinator.async_add_listener(self.async_write_ha_state)
