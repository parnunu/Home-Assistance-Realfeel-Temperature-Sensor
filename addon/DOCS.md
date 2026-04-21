# RealFeel Temperature

The RealFeel Temperature source project is a Home Assistant custom integration, not a native add-on. This published add-on is a compatibility installer that copies the integration files into your Home Assistant configuration so the central repository can remain the only repository URL you paste into Home Assistant.

## Install through the central repo

1. Add `https://github.com/parnunu/home-assistant-addons` to Home Assistant as a custom add-on repository.
2. Install **RealFeel Temperature**.
3. Start the add-on once.
4. Restart Home Assistant.
5. Go to **Settings -> Devices & Services -> Add Integration** and add **RealFeel Temperature**.

## What it installs

The add-on copies:

- `custom_components/realfeel_temperature`

into:

- `/config/custom_components/realfeel_temperature`

inside your Home Assistant configuration directory.

## Notes

- Re-running the add-on refreshes the installed integration files from this source repository.
- This is a compatibility path for a custom integration source repo. It is not a long-running service.
- After the files are copied, the add-on exits successfully. That is expected.

## Source of truth

The integration source code remains in this repository:

- `custom_components/realfeel_temperature`

The central add-on repository only receives the published installer folder:

- `realfeel_temperature/`
