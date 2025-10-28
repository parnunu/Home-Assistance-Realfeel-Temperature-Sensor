"""Sensor platform for the RealFeel Temperature integration."""

from __future__ import annotations

from math import exp
from typing import Any, Callable

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
  ATTR_HUMIDITY_SOURCE,
  ATTR_TEMPERATURE_SOURCE,
  ATTR_WIND_SOURCE,
  ATTR_WIND_UNIT,
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
  MANUFACTURER,
  MODEL,
  SOFTWARE_VERSION,
  WIND_UNITS,
)


async def async_setup_entry(
  hass: HomeAssistant,
  entry: ConfigEntry,
  async_add_entities: AddEntitiesCallback,
) -> None:
  """Set up the sensor entry."""
  async_add_entities([RealFeelSensor(hass, entry)])


class RealFeelSensor(SensorEntity):
  """Representation of the RealFeel temperature sensor."""
  
  _attr_should_poll = False
  _attr_device_class = SensorDeviceClass.TEMPERATURE
  _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
  
  def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Initialize the sensor."""
    self.hass = hass
    self.entry = entry
    self._attr_name = entry.data.get(CONF_NAME, DEFAULT_NAME)
    self._attr_unique_id = entry.entry_id
    self._attr_extra_state_attributes: dict[str, Any] = {}
    self._unsubscribers: list[Callable[[], None]] = []
  
  async def async_added_to_hass(self) -> None:
    """Handle when the entity is added to Home Assistant."""
    await super().async_added_to_hass()
    for entity_id in self._tracked_entities:
      if entity_id:
        unsub = async_track_state_change_event(
          self.hass,
          [entity_id],
          self._handle_source_state_event,
        )
        self._unsubscribers.append(unsub)
    await self._async_update_state()
  
  async def async_will_remove_from_hass(self) -> None:
    """Handle entity removal."""
    for unsub in self._unsubscribers:
      unsub()
    self._unsubscribers.clear()
  
  @property
  def device_info(self) -> dict[str, Any]:
    """Return device information for the virtual device."""
    return {
      "identifiers": {(DOMAIN, self.entry.entry_id)},
      "manufacturer": MANUFACTURER,
      "model": MODEL,
      "name": self.entry.data.get(CONF_NAME, DEFAULT_NAME),
      "sw_version": SOFTWARE_VERSION,
    }
  
  @property
  def _tracked_entities(self) -> list[str | None]:
    """Return the list of tracked entity ids."""
    return [
      self.entry.data.get(CONF_TEMPERATURE_ENTITY),
      self.entry.data.get(CONF_HUMIDITY_ENTITY),
      self.entry.data.get(CONF_WIND_ENTITY),
    ]
  
  @callback
  async def _handle_source_state_event(self, event) -> None:
    """Handle source entity state changes."""
    await self._async_update_state()
  
  async def _async_update_state(self) -> None:
    """Update the sensor state."""
    data = self.entry.data
    temperature_value, temperature_source = self._resolve_value(
      data.get(CONF_TEMPERATURE_ENTITY),
      float(data.get(CONF_TEMPERATURE_FALLBACK, DEFAULT_TEMPERATURE)),
      "°C",
    )
    humidity_value, humidity_source = self._resolve_value(
      data.get(CONF_HUMIDITY_ENTITY),
      float(data.get(CONF_HUMIDITY_FALLBACK, DEFAULT_HUMIDITY)),
      "%",
    )
    humidity_value = max(0.0, min(100.0, humidity_value))
    wind_unit = data.get(CONF_WIND_UNIT, WIND_UNITS[0])
    wind_value, wind_source = self._resolve_value(
      data.get(CONF_WIND_ENTITY),
      float(data.get(CONF_WIND_FALLBACK, DEFAULT_WIND)),
      wind_unit,
    )
    wind_mps = self._convert_wind_to_mps(wind_value, wind_unit)
    e_term = (humidity_value / 100.0) * 6.105 * exp(17.27 * temperature_value / (237.7 + temperature_value))
    apparent_temperature = temperature_value + 0.33 * e_term - 0.70 * wind_mps - 4.0
    self._attr_native_value = round(apparent_temperature, 2)
    self._attr_extra_state_attributes = {
      ATTR_TEMPERATURE_SOURCE: temperature_source,
      ATTR_HUMIDITY_SOURCE: humidity_source,
      ATTR_WIND_SOURCE: wind_source,
      ATTR_WIND_UNIT: wind_unit,
    }
    self.async_write_ha_state()
  
  def _resolve_value(
    self,
    entity_id: str | None,
    fallback: float,
    unit: str,
  ) -> tuple[float, str]:
    """Resolve a numeric value from an entity or fallback."""
    if entity_id:
      state = self.hass.states.get(entity_id)
      if state and state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
        try:
          value = float(state.state)
        except (TypeError, ValueError):
          value = None
        else:
          return value, entity_id
    return fallback, f"fallback: {fallback:.2f} {unit}"
  
  def _convert_wind_to_mps(self, value: float, unit: str) -> float:
    """Convert wind speed into meters per second."""
    if unit == "km/h":
      return value / 3.6
    if unit == "knots":
      return value * 0.514444
    return value
