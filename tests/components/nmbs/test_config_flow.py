"""Test the NMBS config flow."""

from copy import deepcopy
from typing import Any
from unittest.mock import patch

import pytest

from homeassistant import config_entries
from homeassistant.components.nmbs.const import (
    CONF_STATION_FROM,
    CONF_STATION_LIVE,
    CONF_STATION_TO,
    DOMAIN,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from . import mocked_request_function

DUMMY_DATA: dict[str, Any] = {
    "STAT_BRUSSELS_NORTH": "BE.NMBS.008812005",
    "STAT_BRUSSELS_CENTRAL": "BE.NMBS.008813003",
    "STAT_BRUSSELS_SOUTH": "BE.NMBS.008814001",
}


async def test_show_set_form(hass: HomeAssistant) -> None:
    """Test that the setup form is served."""
    with patch(
        "pyrail.irail.iRail.get_stations",
        wraps=mocked_request_function,
    ):
        result: dict[str, Any] = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

        assert result["type"] is FlowResultType.MENU
        assert result["menu_options"] == {"connection", "liveboard"}
        assert result["step_id"] == "choose"


async def test_step_liveboard_no_data(hass: HomeAssistant) -> None:
    """Test starting a flow by user which chooses for liveboard."""
    with patch(
        "pyrail.irail.iRail.get_stations",
        wraps=mocked_request_function,
    ):
        result: dict[str, Any] = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"next_step_id": "liveboard"},
        )

        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {}


@pytest.mark.parametrize(
    "user_input",
    [
        {CONF_STATION_LIVE: deepcopy(DUMMY_DATA["STAT_BRUSSELS_CENTRAL"])},
    ],
)
async def test_step_liveboard_data(
    hass: HomeAssistant, user_input: dict | None
) -> None:
    """Test starting a flow by user which filled in data for liveboard."""
    with patch(
        "pyrail.irail.iRail.get_stations",
        wraps=mocked_request_function,
    ):
        result: dict[str, Any] = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"next_step_id": "liveboard"},
        )

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input,
        )

        await hass.async_block_till_done()
        assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_step_connection_no_data(hass: HomeAssistant) -> None:
    """Test starting a flow by user which chooses for connection."""
    with patch(
        "pyrail.irail.iRail.get_stations",
        wraps=mocked_request_function,
    ):
        result: dict[str, Any] = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"next_step_id": "connection"},
        )

        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {}


@pytest.mark.parametrize(
    "user_input",
    [
        {
            CONF_STATION_FROM: deepcopy(DUMMY_DATA["STAT_BRUSSELS_NORTH"]),
            CONF_STATION_TO: deepcopy(DUMMY_DATA["STAT_BRUSSELS_SOUTH"]),
        }
    ],
)
async def test_step_connection_data(
    hass: HomeAssistant, user_input: dict | None
) -> None:
    """Test starting a flow by user which filled in data for connection."""
    with patch(
        "pyrail.irail.iRail.get_stations",
        wraps=mocked_request_function,
    ):
        result: dict[str, Any] = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"next_step_id": "connection"},
        )

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input,
        )

        await hass.async_block_till_done()
        assert result["type"] is FlowResultType.CREATE_ENTRY
