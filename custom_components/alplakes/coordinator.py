import asyncio
import json
import logging
from datetime import UTC, datetime, timedelta

import aiohttp

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    BASE_URL,
    DEFAULT_MODEL,
    LAKE_API_ID_BY_LAKE,
    MODEL_BY_LAKE,
    ONE_D_BASE_URL,
    ONE_D_LAKE_IDS,
    ONE_D_MODEL,
)

_LOGGER = logging.getLogger(__name__)


class LakeDataCoordinator(DataUpdateCoordinator):
    def __init__(
        self, hass, lake, latitude, longitude, depth, scan_interval, location_name
    ):
        super().__init__(
            hass,
            logger=_LOGGER,
            name="AlplakesCoordinator",
            update_interval=timedelta(minutes=scan_interval),
        )

        self.lake = lake
        self.api_lake = LAKE_API_ID_BY_LAKE.get(lake, lake)
        self.is_1d = self.api_lake in ONE_D_LAKE_IDS
        self.model = MODEL_BY_LAKE.get(self.api_lake, DEFAULT_MODEL)
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.location_name = location_name
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        try:
            now = datetime.now(UTC).replace(second=0, microsecond=0)
            start_time = (now - timedelta(hours=4)).strftime("%Y%m%d%H%M")
            end_time = now.strftime("%Y%m%d%H%M")

            variable = "T" if self.is_1d else "temperature"
            if self.is_1d:
                url = (
                    f"{ONE_D_BASE_URL}/{ONE_D_MODEL}/{self.api_lake}/"
                    f"{start_time}/{end_time}/{self.depth}?variables={variable}"
                )
            else:
                url = (
                    f"{BASE_URL}/{self.model}/{self.api_lake}/{start_time}/{end_time}/"
                    f"{self.depth}/{self.latitude}/{self.longitude}"
                    f"?variables={variable}"
                )

            async with self.session.get(url, timeout=10) as resp:
                body = await resp.text()

                if resp.status != 200:
                    _LOGGER.error(
                        "AlpLakes API returned HTTP %s for URL %s. Body: %s",
                        resp.status,
                        url,
                        body[:1000],
                    )
                    raise UpdateFailed(
                        f"HTTP {resp.status} from API. URL: {url}. "
                        f"Body: {body[:500]}"
                    )

                try:
                    data = json.loads(body)
                except Exception as err:
                    _LOGGER.error(
                        "AlpLakes API returned non-JSON response for URL %s. Body: %s",
                        url,
                        body[:1000],
                    )
                    raise UpdateFailed(f"Invalid JSON from API: {err}") from err

            temps = data["variables"][variable]["data"]

            if not temps:
                raise UpdateFailed("No temperature data returned from API")

            return round(float(temps[-1]), 1)

        except UpdateFailed:
            raise

        except (
            asyncio.TimeoutError,
            aiohttp.ClientError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ) as err:
            raise UpdateFailed(f"Failed to fetch or parse data: {err}") from err
