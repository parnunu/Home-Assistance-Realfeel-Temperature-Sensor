# RealFeel Temperature Sensor for Home Assistant

A custom Home Assistant integration that calculates an apparent temperature sensor by combining your existing temperature, humidity, and wind speed data. The integration provides a responsive helper entity that better reflects how outdoor conditions actually feel, even when some of your source sensors are temporarily unavailable.

## Features

- Calculates apparent temperature using temperature, humidity, and wind speed inputs.
- Listens to entity state changes so the RealFeel value updates instantly without polling.
- Allows individual fallback values to keep the calculation working when any source sensor is missing or unavailable.
- Exposes source information as sensor attributes to make troubleshooting simple.
- Supports wind speed in metres per second, kilometres per hour, or knots.

## Installation

### Manual installation

1. Copy the `custom_components/realfeel_temperature` folder into the `custom_components` directory of your Home Assistant configuration.
2. Restart Home Assistant.

### HACS (custom repository)

If you use [HACS](https://hacs.xyz/), add this repository as a custom integration source and install **RealFeel Temperature**. Restart Home Assistant when prompted.

## Configuration

1. In Home Assistant, go to **Settings → Devices & Services**.
2. Select **+ Add Integration** and search for **RealFeel Temperature**.
3. Choose the temperature, humidity, and wind speed entities you want the integration to use. Each input is optional—provide what you have available.
4. Optionally override the fallback values. These defaults are used whenever an entity is missing or reports an unknown/unavailable state:
   - Temperature fallback: `25 °C`
   - Humidity fallback: `60 %`
   - Wind fallback: `0.5` (in the selected unit)
5. Pick the wind speed unit (metres per second, kilometres per hour, or knots).
6. Confirm to create the helper entity.

You can revisit the integration’s **Options** to adjust entities, fallbacks, or units at any time. All numeric inputs are coerced to floats, ensuring the calculation runs consistently.

## How it works

The integration tracks each configured source entity and recalculates the RealFeel temperature whenever any of them changes. When wind speed is supplied in kilometres per hour or knots it is converted to metres per second internally before applying the formula. The resulting value is rounded to two decimal places.

The sensor exposes the following extra state attributes:

| Attribute | Description |
| --- | --- |
| `temperature_source` | Entity ID or fallback string used for temperature input. |
| `humidity_source` | Entity ID or fallback string used for humidity input. |
| `wind_source` | Entity ID or fallback string used for wind input. |
| `wind_unit` | Wind speed unit used for the latest calculation. |

## Troubleshooting

- If the sensor shows `unavailable`, confirm that Home Assistant was restarted after installation and that the integration is enabled.
- Verify that any referenced entities are numeric sensors. Non-numeric values are ignored in favour of the fallback value.
- Adjust fallback values to better match your local baseline when a sensor is offline for long periods.

## Contributing

Pull requests and issue reports are welcome. Please keep the coding style consistent with Home Assistant’s guidelines and include reproduction steps when reporting a bug.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
