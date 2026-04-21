ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION="Install or refresh the RealFeel Temperature custom integration in Home Assistant."
ARG BUILD_NAME="RealFeel Temperature"
ARG BUILD_REF
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    maintainer="parnunu" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.documentation="https://github.com/parnunu/Home-Assistance-Realfeel-Temperature-Sensor" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.source="https://github.com/parnunu/Home-Assistance-Realfeel-Temperature-Sensor" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.version="${BUILD_VERSION}"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apk add --no-cache \
    bash \
    coreutils

COPY custom_components/realfeel_temperature /opt/realfeel_temperature
COPY addon/run.sh /run.sh
RUN chmod 755 /run.sh

CMD ["/run.sh"]
