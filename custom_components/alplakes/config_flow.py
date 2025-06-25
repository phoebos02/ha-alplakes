# config_flow.py
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, VALID_LAKES, DEFAULT_LAKE, DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_DEPTH, DEFAULT_SCAN_INTERVAL

class AlplakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Alpine Lakes Temperature."""

    VERSION = 1

    def __init__(self):
        self.data = {}

    async def async_step_user(self, user_input=None):
        """Step 1: User provides lake, latitude, longitude, depth, scan_interval."""
        if user_input is None:
            data_schema = vol.Schema({
                vol.Required("lake", default=DEFAULT_LAKE): vol.In(VALID_LAKES),
                vol.Required("latitude", default=DEFAULT_LATITUDE): float,
                vol.Required("longitude", default=DEFAULT_LONGITUDE): float,
                vol.Required("depth", default=DEFAULT_DEPTH): float,
                vol.Required("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
            })
            return self.async_show_form(step_id="user", data_schema=data_schema)

        self.data = user_input

        unique_id = f"Lake_{self.data['lake']}_{self.data['latitude']}_{self.data['longitude']}_{self.data['depth']}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"Lake {self.data['lake']} ({self.data['latitude']}, {self.data['longitude']})",
            data=self.data,
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
        initial_interval = self.config_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        if user_input is None:
            data_schema = vol.Schema({
                vol.Required("scan_interval", default=initial_interval): int,
            })
            return self.async_show_form(step_id="init", data_schema=data_schema)

        return self.async_create_entry(
            title="",
            data={"scan_interval": user_input["scan_interval"]},
        )
