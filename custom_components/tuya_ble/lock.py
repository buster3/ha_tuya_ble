from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.lock import LockEntity, LockEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .devices import TuyaBLEData, TuyaBLEEntity, TuyaBLEProductInfo
from .tuya_ble import TuyaBLEDevice

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Tuya BLE lock."""
    data: TuyaBLEData = hass.data[DOMAIN][entry.entry_id]
    
    description = LockEntityDescription(
        key="lock",
        name="Lock",
    )
    
    async_add_entities([TuyaBLELock(hass, data.coordinator, data.device, data.product, description)])

class TuyaBLELock(TuyaBLEEntity, LockEntity):
    """Representation of a Tuya BLE lock."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: Any,
        device: TuyaBLEDevice,
        product: TuyaBLEProductInfo,
        description: LockEntityDescription,
    ) -> None:
        super().__init__(hass, coordinator, device, product, description)

    @property
    def is_locked(self) -> bool:
        """Return true if lock is locked."""
        # DP 1 is the status (1=Locked, 0=Unlocked)
        status = self._device.datapoints.get(1)
        return status.value == 1 if status else False

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the device."""
        await self._device.send_command(1, 1)

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the device."""
        await self._device.send_command(1, 0)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
