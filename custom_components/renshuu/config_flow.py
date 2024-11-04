import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
import aiohttp

from .const import DOMAIN, CONF_API_KEY, API_PROFILE_ENDPOINT

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            valid = await self._test_credentials(
                self.hass, user_input[CONF_API_KEY]
            )

            if valid:
                return self.async_create_entry(
                    title="Renshuu API Key",
                    data={
                        CONF_API_KEY: user_input[CONF_API_KEY],
                    },
                )
            else:
                errors["base"] = "Failed to authenticate"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                }
            ),
            errors=errors,
        )

    async def _test_credentials(self, hass: HomeAssistant, api_key: str) -> bool:
        try:
            session = aiohttp_client.async_get_clientsession(hass)
            headers = {"Authorization": f"Bearer {api_key}"}

            endpoint = API_PROFILE_ENDPOINT
            async with session.get(endpoint, headers=headers) as response:
                return response.status == 200
        except aiohttp.ClientError:
            return False
