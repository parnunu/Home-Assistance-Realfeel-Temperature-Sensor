"""RealFeel Temperature integration setup."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS = [Platform.SENSOR]


def _ensure_domain_data(hass: HomeAssistant) -> None:
  """Ensure the domain data container exists."""
  hass.data.setdefault(DOMAIN, {})


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
  """Set up the RealFeel Temperature integration."""
  _ensure_domain_data(hass)
  return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  """Set up a config entry for the integration."""
  _ensure_domain_data(hass)
  hass.data[DOMAIN][entry.entry_id] = {}
  entry.async_on_unload(entry.add_update_listener(_async_update_listener))
  await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
  return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  """Unload a config entry for the integration."""
  unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
  if unload_ok:
    hass.data[DOMAIN].pop(entry.entry_id, None)
  return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
  """Handle config entry updates by reloading platforms."""
  await hass.config_entries.async_reload(entry.entry_id)
