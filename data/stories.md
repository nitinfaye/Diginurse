## Select round type - Configure
* affirm
  - action_round
  - slot{"round": "configure"}
  - action_improve_experience
> ask_configure

## Select round type - new_treatment
* deny
  - action_round
  - slot{"round": "new_treatment"}
  - action_recommend
> ask_change_anything

## Select round type - new_treatment - change time - affirm
> ask_change_anything
* affirm
  - form_changes
  - form{"name": "form_changes"}
  - form{"name": null}
  - action_recommend

## Select round type - new_treatment - affirm
* affirm
  - action_round
  - slot{"round": "new_treatment"}
  - form_changes
  - form{"name": "form_changes"}
  - form{"name": null}
  - action_recommend

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

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
