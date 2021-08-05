import { HomeAssistant } from "custom-card-helpers/dist/types";
import { HassEntity } from "home-assistant-js-websocket";
import { listVariable } from "../data/variables/list_variable";
import { computeStateDisplay } from "custom-card-helpers";

export const sunStates = (hass: HomeAssistant, stateObj: HassEntity) =>
  listVariable({
    options: [
      {
        value: "below_horizon",
        name: computeStateDisplay(hass.localize, { ...stateObj, state: "below_horizon" }, hass.language),
        icon: "hass:weather-sunny-off"
      },
      {
        value: "above_horizon",
        name: computeStateDisplay(hass.localize, { ...stateObj, state: "above_horizon" }, hass.language),
        icon: "hass:weather-sunny"
      },
    ]
  })