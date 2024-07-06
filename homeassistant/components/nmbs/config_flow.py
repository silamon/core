"""Config flow for NMBS integration."""

from typing import Any

from pyrail import iRail
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_NAME, CONF_TYPE
from homeassistant.core import DOMAIN as HOMEASSISTANT_DOMAIN
from homeassistant.data_entry_flow import AbortFlow
from homeassistant.helpers.issue_registry import IssueSeverity, async_create_issue
from homeassistant.helpers.selector import (
    BooleanSelector,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_EXCLUDE_VIAS,
    CONF_SHOW_ON_MAP,
    CONF_STATION_FROM,
    CONF_STATION_LIVE,
    CONF_STATION_TO,
    DOMAIN,
)


class NMBSConfigFlow(ConfigFlow, domain=DOMAIN):
    """NMBS config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        self.api_client = iRail()
        self.stations: Any | None = None

    async def _fetch_stations_choices(self):
        """Fetch the stations."""

        if self.stations is None:
            self.stations = await self.hass.async_add_executor_job(
                self.api_client.get_stations
            )
        return [
            SelectOptionDict(value=station["id"], label=station["name"])
            for station in self.stations["station"]
        ]

    async def _fetch_station_for_id(self, station_id: str) -> Any | None:
        station = next(
            (
                station
                for station in self.stations["station"]
                if station.get("id") == station_id
            ),
            None,
        )
        return station["name"]

    async def async_step_user(
        self, _: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        return await self.async_step_choose()

    async def async_step_choose(
        self, _: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the step to choose what to setup."""
        return self.async_show_menu(
            step_id="choose", menu_options={"liveboard", "connection"}
        )

    async def async_step_liveboard(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the step to setup a liveboard."""

        errors: dict = {}
        if user_input is not None:
            await self.async_set_unique_id(f"{user_input[CONF_STATION_LIVE]}")
            self._abort_if_unique_id_configured()

            user_input[CONF_TYPE] = "liveboard"
            config_entry_name = user_input[CONF_NAME]
            if config_entry_name == "":
                config_entry_name = (
                    f"{await self._fetch_station_for_id(user_input[CONF_STATION_LIVE])}"
                )
            return self.async_create_entry(
                title=config_entry_name,
                data=user_input,
            )

        return self.async_show_form(
            step_id="liveboard",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=""): str,
                    vol.Required(CONF_STATION_LIVE): SelectSelector(
                        SelectSelectorConfig(
                            options=await self._fetch_stations_choices(),
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(CONF_SHOW_ON_MAP, default=False): BooleanSelector(),
                },
            ),
            errors=errors,
        )

    async def async_step_connection(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the step to setup a connection between 2 stations."""

        errors: dict = {}
        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_STATION_FROM]}-{user_input[CONF_STATION_TO]}"
            )
            self._abort_if_unique_id_configured()

            user_input[CONF_TYPE] = "connection"
            config_entry_name = user_input[CONF_NAME]
            if config_entry_name == "":
                config_entry_name = f"{await self._fetch_station_for_id(user_input[CONF_STATION_FROM])}-{await self._fetch_station_for_id(user_input[CONF_STATION_TO])}"
            return self.async_create_entry(
                title=config_entry_name,
                data=user_input,
            )

        choices = await self._fetch_stations_choices()
        return self.async_show_form(
            step_id="connection",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=""): str,
                    vol.Required(CONF_STATION_FROM): SelectSelector(
                        SelectSelectorConfig(
                            options=choices,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Required(CONF_STATION_TO): SelectSelector(
                        SelectSelectorConfig(
                            options=choices,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    ),
                    vol.Optional(CONF_EXCLUDE_VIAS, default=False): BooleanSelector(),
                    vol.Optional(CONF_SHOW_ON_MAP, default=False): BooleanSelector(),
                },
            ),
            errors=errors,
        )

    async def async_step_import(self, user_input: dict[str, Any]) -> ConfigFlowResult:
        """Import configuration from yaml."""

        def create_repair(error: str | None = None) -> None:
            async_create_issue(
                self.hass,
                HOMEASSISTANT_DOMAIN,
                f"deprecated_yaml_{DOMAIN}",
                breaks_in_ha_version="2025.3.0",
                is_fixable=False,
                issue_domain=DOMAIN,
                severity=IssueSeverity.WARNING,
                translation_key="deprecated_yaml",
                translation_placeholders={
                    "domain": DOMAIN,
                    "integration_title": "NMBS",
                },
            )

        connection_user_input: dict = {
            CONF_TYPE: "connection",
            CONF_STATION_FROM: user_input[CONF_STATION_FROM],
            CONF_STATION_TO: user_input[CONF_STATION_TO],
            CONF_NAME: user_input[CONF_NAME],
            CONF_EXCLUDE_VIAS: user_input[CONF_EXCLUDE_VIAS],
            CONF_SHOW_ON_MAP: user_input[CONF_SHOW_ON_MAP],
        }

        if CONF_STATION_LIVE in user_input:
            liveboard_user_input = {
                CONF_TYPE: "liveboard",
                CONF_STATION_LIVE: user_input[CONF_STATION_LIVE],
                CONF_SHOW_ON_MAP: user_input[CONF_SHOW_ON_MAP],
                CONF_NAME: user_input[CONF_NAME],
            }

            try:
                result = await self.async_step_liveboard(liveboard_user_input)
            except AbortFlow as ex:
                if ex.reason == "already_configured":
                    create_repair()
                raise ex

        try:
            result = await self.async_step_connection(connection_user_input)
        except AbortFlow as ex:
            if ex.reason == "already_configured":
                create_repair()
            raise ex

        create_repair()
        return result
