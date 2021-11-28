## DigiNurse flows
* digi_nurse_flow
  - action_round
  - slot{"round": "configure"}
  - action_configure_flow

* digi_nurse_flow
  - action_round
  - slot{"round": "new_treatment"}
  - action_new_treatment_flow

* digi_nurse_flow
  - action_round
  - slot{"round": "regular_nursing"}
  - action_regular_nursing_round_flow

## Select round type - Configure
* affirm
  - slot{"round": "configure"}
  - action_improve_experience
> ask_configure

## Select round type - Configure
* deny
  - slot{"round": "configure"}
  - action_comeback_later

## Select round type - new_treatment
* deny
  - slot{"round": "new_treatment"}
  - action_recommend
> ask_change_anything

> ask_change_anything
* deny
  - action_deny_recommend

> ask_change_anything
* affirm
  - form_changes
  - form{"name": "form_changes"}
  - form{"name": null}
  - action_recommend

## Select round type - new_treatment - affirm
* affirm
  - slot{"round": "new_treatment"}
  - form_changes
  - form{"name": "form_changes"}
  - form{"name": null}
  - action_recommend
> ask_change_anything

## Select round type - new_treatment - deny
> ask_change_anything
* deny
  - action_deny_recommend

## Affirm improve experience
> ask_configure
* affirm
  - form_sleep_time
  - form{"name": "form_sleep_time"}
  - form{"name": null}
  - form_meal_time
  - form{"name": "form_meal_time"}
  - form{"name": null}
  - form_ask_smoke
  - form{"name": "form_ask_smoke"}
  - form{"name": null}
  - form_ask_drink
  - form{"name": "form_ask_drink"}
  - form{"name": null}
  - form_ask_workout
  - form{"name": "form_ask_workout"}
  - form{"name": null}

## Deny 
> ask_configure
* deny
  - action_thank_you

## Affirm change anything - no
> ask_change_anything

## ask how feeling now
* better
 - action_last_sleep_night
> last_sleep_night

## apologize feeling worst - ask doctor support
* not_better OR worse
  - form_doctor_support
  - form{"name": "form_doctor_support"}
  - form{"name": null}
  - action_last_sleep_night
> last_sleep_night

## Pre meal - Post meal
> last_sleep_night
* all_fine OR worse
  - form_pre_post_meal
  - form{"name":"form_pre_post_meal"}
  - form{"name": null}
  - action_thank_you

* change_time
  - action_round
  - action_ask_changes

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
