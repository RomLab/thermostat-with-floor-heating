import { HomeAssistant } from "custom-card-helpers/dist/types";
import { HassEntity } from "home-assistant-js-websocket";
import { listVariable } from "../data/variables/list_variable";

export const personStates = (hass: HomeAssistant, _stateObj: HassEntity) => listVariable({
  options: [
    {
      value: "home",
      name: hass.localize("state_badge.person.home", hass.language),
      icon: 'hass:home-outline',
    },
    {
      value: "not_home",
      name: hass.localize("state_badge.person.not_home", hass.language),
      icon: 'hass:exit-run'
    }
  ]
});