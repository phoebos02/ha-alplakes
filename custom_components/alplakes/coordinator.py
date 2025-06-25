import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta, UTC
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import BASE_URL, MODEL

class LakeDataCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, lake, latitude, longitude, depth, scan_interval):
        logger = hass.logger if hass is not None else logging.getLogger(__name__)
        super().__init__(hass, logger=logger, name="AlplakesCoordinator", update_interval=timedelta(minutes=scan_interval))
        self.lake = lake
        self.latitude = latitude
        self.longitude = longitude
        self.depth = depth
        self.session = aiohttp.ClientSession()

    async def _async_update_data(self):
        try:
            now = datetime.now(UTC).replace(second=0, microsecond=0)
            start_time = (now - timedelta(hours=4)).strftime("%Y%m%d%H%M")
            end_time = now.strftime("%Y%m%d%H%M")

            url = f"{BASE_URL}/{MODEL}/{self.lake}/{start_time}/{end_time}/{self.depth}/{self.latitude}/{self.longitude}?variables=temperature"
            async with self.session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"HTTP {resp.status} from API")

                data = await resp.json()
                temps = data["variables"]["temperature"]["data"]
                if not temps:
                    raise UpdateFailed("No temperature data returned from API")
                temp = temps[-1]  # Take the last data point
                return round(float(temp), 1)

        except UpdateFailed:
            raise
        except (asyncio.TimeoutError, aiohttp.ClientError, KeyError, IndexError, ValueError) as e:
            raise UpdateFailed(f"Failed to fetch or parse data: {e}")

    async def async_will_remove_from_hass(self):
        await self.session.close()
