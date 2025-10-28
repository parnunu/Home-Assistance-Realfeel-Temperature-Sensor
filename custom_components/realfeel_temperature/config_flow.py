"""Config flow for the RealFeel Temperature integration."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
  EntitySelector,
  EntitySelectorConfig,
  NumberSelector,
  NumberSelectorConfig,
  NumberSelectorMode,
  SelectSelector,
  SelectSelectorConfig,
  SelectSelectorMode,
  TextSelector,
  TextSelectorConfig,
  TextSelectorType,
)

from .const import (
  CONF_HUMIDITY_ENTITY,
  CONF_HUMIDITY_FALLBACK,
  CONF_NAME,
  CONF_TEMPERATURE_ENTITY,
  CONF_TEMPERATURE_FALLBACK,
  CONF_WIND_ENTITY,
  CONF_WIND_FALLBACK,
  CONF_WIND_UNIT,
  DEFAULT_HUMIDITY,
  DEFAULT_NAME,
  DEFAULT_TEMPERATURE,
  DEFAULT_WIND,
  DOMAIN,
  WIND_UNITS,
)


def _build_schema(current: dict | None = None) -> vol.Schema:
  """Build the shared configuration schema."""
  current = current or {}
  return vol.Schema(
    {
      vol.Optional(
        CONF_NAME,
        default=current.get(CONF_NAME, DEFAULT_NAME),
      ): TextSelector(TextSelectorConfig(type=TextSelectorType.TEXT)),
      vol.Optional(
        CONF_TEMPERATURE_ENTITY,
        default=current.get(CONF_TEMPERATURE_ENTITY),
      ): EntitySelector(
        EntitySelectorConfig(domain="sensor", device_class="temperature"),
      ),
      vol.Optional(
        CONF_TEMPERATURE_FALLBACK,
        default=current.get(CONF_TEMPERATURE_FALLBACK, DEFAULT_TEMPERATURE),
      ): NumberSelector(
        NumberSelectorConfig(
          min=-80,
          max=80,
          step=0.1,
          mode=NumberSelectorMode.BOX,
        ),
      ),
      vol.Optional(
        CONF_HUMIDITY_ENTITY,
        default=current.get(CONF_HUMIDITY_ENTITY),
      ): EntitySelector(
        EntitySelectorConfig(domain="sensor", device_class="humidity"),
      ),
      vol.Optional(
        CONF_HUMIDITY_FALLBACK,
        default=current.get(CONF_HUMIDITY_FALLBACK, DEFAULT_HUMIDITY),
      ): NumberSelector(
        NumberSelectorConfig(
          min=0,
          max=100,
          step=1,
          mode=NumberSelectorMode.BOX,
        ),
      ),
      vol.Optional(
        CONF_WIND_ENTITY,
        default=current.get(CONF_WIND_ENTITY),
      ): EntitySelector(
        EntitySelectorConfig(domain="sensor"),
      ),
      vol.Optional(
        CONF_WIND_FALLBACK,
        default=current.get(CONF_WIND_FALLBACK, DEFAULT_WIND),
      ): NumberSelector(
        NumberSelectorConfig(
          min=0,
          max=60,
          step=0.1,
          mode=NumberSelectorMode.BOX,
        ),
      ),
      vol.Optional(
        CONF_WIND_UNIT,
        default=current.get(CONF_WIND_UNIT, WIND_UNITS[0]),
      ): SelectSelector(
        SelectSelectorConfig(options=WIND_UNITS, mode=SelectSelectorMode.DROPDOWN),
      ),
    },
  )


class RealfeelTemperatureConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
  """Handle a config flow for the integration."""
  
  VERSION = 1
  
  async def async_step_user(self, user_input: dict | None = None):
    """Handle the initial step."""
    errors: dict[str, str] = {}
    if user_input is not None:
      data = dict(user_input)
      name = data.get(CONF_NAME) or DEFAULT_NAME
      data[CONF_NAME] = name
      data[CONF_TEMPERATURE_FALLBACK] = float(data[CONF_TEMPERATURE_FALLBACK])
      data[CONF_HUMIDITY_FALLBACK] = float(data[CONF_HUMIDITY_FALLBACK])
      data[CONF_WIND_FALLBACK] = float(data[CONF_WIND_FALLBACK])
      return self.async_create_entry(title=name, data=data)
    return self.async_show_form(
      step_id="user",
      data_schema=_build_schema(),
      errors=errors,
    )
  
  @staticmethod
  @callback
  def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
    """Return the options flow handler."""
    return RealfeelTemperatureOptionsFlowHandler(config_entry)


class RealfeelTemperatureOptionsFlowHandler(config_entries.OptionsFlow):
  """Handle options for the integration."""
  
  def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
    """Initialize the options flow handler."""
    self.config_entry = config_entry
  
  async def async_step_init(self, user_input: dict | None = None):
    """Manage the options form."""
    if user_input is not None:
      updated = dict(self.config_entry.data)
      updated.update(user_input)
      updated[CONF_NAME] = updated.get(CONF_NAME) or DEFAULT_NAME
      updated[CONF_TEMPERATURE_FALLBACK] = float(updated[CONF_TEMPERATURE_FALLBACK])
      updated[CONF_HUMIDITY_FALLBACK] = float(updated[CONF_HUMIDITY_FALLBACK])
      updated[CONF_WIND_FALLBACK] = float(updated[CONF_WIND_FALLBACK])
      self.hass.config_entries.async_update_entry(self.config_entry, data=updated)
      await self.hass.config_entries.async_reload(self.config_entry.entry_id)
      return self.async_create_entry(title="", data={})
    return self.async_show_form(
      step_id="init",
      data_schema=_build_schema(self.config_entry.data),
    )
