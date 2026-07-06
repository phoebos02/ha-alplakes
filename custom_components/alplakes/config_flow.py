import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DEFAULT_DEPTH,
    DEFAULT_LAKE,
    DEFAULT_LATITUDE,
    DEFAULT_LOCATION_NAME,
    DEFAULT_LONGITUDE,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    VALID_LAKES,
)
from .helpers import make_measurement_id, sanitize_location_name


def _user_schema():
    return vol.Schema(
        {
            vol.Required("lake", default=DEFAULT_LAKE): vol.In(VALID_LAKES),
            vol.Required("location_name", default=DEFAULT_LOCATION_NAME): str,
            # Coerce types here but perform range checks in the step
            vol.Required("latitude", default=DEFAULT_LATITUDE): vol.Coerce(float),
            vol.Required("longitude", default=DEFAULT_LONGITUDE): vol.Coerce(float),
            vol.Required("depth", default=DEFAULT_DEPTH): vol.Coerce(float),
            vol.Required("scan_interval", default=DEFAULT_SCAN_INTERVAL): vol.Coerce(int),
        }
    )


class AlplakesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Alpine Lakes Temperature."""

    VERSION = 1

    def __init__(self):
        self.data = {}

    async def async_step_user(self, user_input=None):
        """Step 1: User provides lake, latitude, longitude, depth, scan_interval."""
        data_schema = _user_schema()
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=data_schema)

        try:
            self.data = dict(data_schema(user_input))
        except vol.Invalid as err:
            errors = {
                str(err.path[0]) if err.path else "base": "invalid"
            }
            return self.async_show_form(
                step_id="user", data_schema=data_schema, errors=errors
            )

        # Manual range validation so Home Assistant doesn't raise InvalidData
        errors = {}
        try:
            latitude = float(self.data.get("latitude"))
        except (TypeError, ValueError):
            errors["latitude"] = "invalid"
            latitude = None

        try:
            longitude = float(self.data.get("longitude"))
        except (TypeError, ValueError):
            errors["longitude"] = "invalid"
            longitude = None

        try:
            depth = float(self.data.get("depth"))
        except (TypeError, ValueError):
            errors["depth"] = "invalid"
            depth = None

        try:
            scan_interval = int(self.data.get("scan_interval"))
        except (TypeError, ValueError):
            errors["scan_interval"] = "invalid"
            scan_interval = None

        if latitude is not None and not (-90 <= latitude <= 90):
            errors["latitude"] = "invalid"

        if longitude is not None and not (-180 <= longitude <= 180):
            errors["longitude"] = "invalid"

        if depth is not None and depth < 0:
            errors["depth"] = "invalid"

        if scan_interval is not None and scan_interval < 1:
            errors["scan_interval"] = "invalid"

        if errors:
            return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

        # Normalize and continue
        self.data["location_name"] = sanitize_location_name(self.data["location_name"])

        unique_id = make_measurement_id(
            self.data["lake"],
            self.data["location_name"],
            self.data["latitude"],
            self.data["longitude"],
            self.data["depth"],
        )
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=(
                f"Lake {self.data['lake'].capitalize()} - "
                f"{self.data['location_name'].capitalize()} "
                f"({self.data['latitude']}, {self.data['longitude']})"
            ),
            data=self.data,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AlplakesOptionsFlowHandler()


class AlplakesOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    async def async_step_init(self, user_input=None):
        """Present a form to update scan_interval."""
        initial_interval = self.config_entry.options.get(
            "scan_interval",
            self.config_entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL),
        )

        if user_input is None:
            data_schema = vol.Schema(
                {
                    vol.Required("scan_interval", default=initial_interval): vol.All(
                        vol.Coerce(int), vol.Range(min=1)
                    ),
                }
            )
            return self.async_show_form(step_id="init", data_schema=data_schema)

        return self.async_create_entry(
            title="",
            data={"scan_interval": user_input["scan_interval"]},
        )
