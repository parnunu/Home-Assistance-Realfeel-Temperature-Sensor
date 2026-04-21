#!/usr/bin/env bash
set -Eeuo pipefail

source /usr/lib/bashio/bashio.sh

readonly SOURCE_DIR="/opt/realfeel_temperature"
readonly TARGET_DIR="/homeassistant/custom_components/realfeel_temperature"

fail() {
    bashio::log.error "$1"
    exit 1
}

main() {
    [[ -d "${SOURCE_DIR}" ]] || fail "Bundled integration files are missing from ${SOURCE_DIR}."
    [[ -d "/homeassistant" ]] || fail "Home Assistant configuration directory is not mounted at /homeassistant."

    mkdir -p "/homeassistant/custom_components"
    rm -rf "${TARGET_DIR}"
    mkdir -p "${TARGET_DIR}"
    cp -R "${SOURCE_DIR}/." "${TARGET_DIR}/"

    bashio::log.info "Installed RealFeel Temperature to ${TARGET_DIR}."
    bashio::log.info "Restart Home Assistant, then add the 'RealFeel Temperature' integration from Settings -> Devices & Services."
}

main "$@"
