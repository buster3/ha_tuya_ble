"""Config flow for Tuya BLE integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS
from .const import (
    DOMAIN,
    CONF_UUID,
    CONF_LOCAL_KEY,
    CONF_CATEGORY,
    CONF_PRODUCT_ID,
    CONF_DEVICE_NAME,
    CONF_PRODUCT_NAME,
    CONF_PRODUCT_MODEL,
)

CONF_DEVICE_ID = "device_id"

class TuyaBLEConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Tuya BLE."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"Tuya Lock ({user_input[CONF_ADDRESS]})",
                data={
                    "access_id": "bypassed",
                    "access_secret": "bypassed",
                    "endpoint": "bypassed",
                    "username": "bypassed",
                    "password": "bypassed",
                    "country_code": "1",
                    "app_type": "smartlife",
                    "auth_type": "custom",
                    CONF_ADDRESS: user_input[CONF_ADDRESS],
                    CONF_DEVICE_ID: user_input[CONF_DEVICE_ID],
                    CONF_LOCAL_KEY: user_input[CONF_LOCAL_KEY],
                    CONF_UUID: user_input[CONF_DEVICE_ID],
                    CONF_CATEGORY: "jtmspro",
                    CONF_PRODUCT_ID: "bypassed",
                    CONF_DEVICE_NAME: "Tuya BLE Lock",
                    CONF_PRODUCT_NAME: "Tuya BLE Lock",
                    CONF_PRODUCT_MODEL: "Tuya BLE Lock",
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): str,
                    vol.Required(CONF_DEVICE_ID): str,
                    vol.Required(CONF_LOCAL_KEY): str,
                }
            ),
            errors=errors,
        )
