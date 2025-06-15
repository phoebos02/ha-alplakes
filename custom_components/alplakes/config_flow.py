# config_flow.py
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

VALID_LAKES = [
    "zurich", "geneva", "biel", "joux", "neuchatel", "thun", "brunnen", "lucerne"
]

class AlplakesConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Alpine Lakes Temperature Sensor."""

    DOMAIN = "alplakes"
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Step 1: User provides lake, latitude, longitude, depth, scan_interval."""
        data_schema = vol.Schema({
            vol.Required("lake", default=user_input.get("lake", "zurich")): vol.In(VALID_LAKES),
            vol.Required("latitude", default=user_input.get("latitude", 47.36539)): float,
            vol.Required("longitude", default=user_input.get("longitude", 8.54305)): float,
            vol.Required("depth", default=user_input.get("depth", 1.0)): float,
            vol.Required("scan_interval", default=user_input.get("scan_interval", 30)): int,
        })

        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=data_schema)

        # Construct a unique ID string to prevent duplicates
        lake = user_input["lake"]
        latitude = user_input["latitude"]
        longitude = user_input["longitude"]
        depth = user_input["depth"]
        unique_id = f"{lake}_{latitude}_{longitude}_{depth}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"{lake.capitalize()} ({latitude}, {longitude}, {depth} m)",
            data={
                "lake": lake,
                "latitude": latitude,
                "longitude": longitude,
                "depth": depth,
                "scan_interval": user_input["scan_interval"],
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AlplakesOptionsFlowHandler(config_entry)


class AlplakesOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options (reconfigure scan_interval)."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Present a form to update only scan_interval."""
        initial_interval = self.config_entry.data.get("scan_interval", 30)
        data_schema = vol.Schema({
            vol.Required("scan_interval", default=user_input.get("scan_interval", initial_interval)): int,
        })

        if user_input is None:
            return self.async_show_form(step_id="init", data_schema=data_schema)

        return self.async_create_entry(
            title="",
            data={"scan_interval": user_input["scan_interval"]},
        )
