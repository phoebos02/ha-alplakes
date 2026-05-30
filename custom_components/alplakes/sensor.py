from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    runtime_data = hass.data[DOMAIN][entry.entry_id]
    coordinator = runtime_data["coordinator"]
    data = runtime_data["config"]

    async_add_entities(
        [
            LakeTemperatureSensor(
                coordinator,
                data["lake"],
                data["location_name"],
                data["latitude"],
                data["longitude"],
                data["depth"],
            )
        ]
    )


class LakeTemperatureSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, lake, location_name, lat, lng, depth):
        super().__init__(coordinator)

        self._attr_unique_id = f"lake_{lake}_temp_{location_name}_{depth}"
        self._attr_name = (
            f"Lake {lake.capitalize()} Temperature "
            f"{location_name.capitalize()} ({depth} m)"
        )
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:coolant-temperature"
        self._attr_attribution = "Data provided by Alplakes / Eawag"

    @property
    def native_value(self):
        return self.coordinator.data

    @property
    def device_info(self):
        return {
            "identifiers": {("alplakes", self.unique_id)},
            "name": (
                f"Alplakes – Lake {self.coordinator.lake.capitalize()} - "
                f"{self.coordinator.location_name.capitalize()}"
            ),
            "manufacturer": "Eawag",
            "model": f"AlpLakes {self.coordinator.model}",
        }
