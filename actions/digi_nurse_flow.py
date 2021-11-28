from db.mongo import Person
import sys
sys.path.append("../")
import logging
from typing import Any, Text, Dict, List, Optional, Tuple

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, Restarted
from datetime import datetime as dt, time
from utils.helper import *
from utils import diginurse_utils as dg
from actions.action_utils import get_name_phone, _yes_no_buttons, _feel_better_buttons


class ActionConfigureFlow(Action):

    def name(self) -> Text:
        return "action_configure_flow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name, phone = get_name_phone(tracker)
        logger.info(f"{__file__} : Round : Configure |  name : {name} | phone : {phone}")

        m1 = f"Hello! {name}! Mr.Gupta has diagnosed you with MRI. Your Diginurse will be with you through out the treatment period overseeing your recovery."
        m2 = "\n\nDuring your treatment period I'll assist you with keep track of your medications, logging your vitals and symptoms and provide you with recommendations on your diet and lifestyle"
        m3 = "\n\nAre you ready to setup your personalized nursing plan? It’ll only take few minutes."

        ask = m1 + m2 + m3

        buttons = button_it(_yes_no_buttons())
        dispatcher.utter_message(text=ask, buttons=buttons)

        return []


class ActionNewTreatmentFlow(Action):

    def name(self) -> Text:
        return "action_new_treatment_flow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name, phone = get_name_phone(tracker)
        logger.info(f"{__file__} : Round : New Treatment |  name : {name} | phone : {phone}")

        m1 = f"Dear {name}! during visit to Hospital, Dr.Gupta has diagnosed with MRI"
        m2 = "\nDuring your treatment period I will help you to get recovered. I will assist you in keeping track of your medication, logging your vitals and symptoms and provide you with recommendations on your diet and lifestyle"
        m3 = "\nHere is the routine and lifestyle you have shared with me last time"
        m3 += "\n" + dg.showSchedule(name, phone)
        m3 += "\nHave you changed anything in your routine or lifestyle from last time?"

        ask =  m1 + m2 + m3

        buttons = button_it(_yes_no_buttons())
        dispatcher.utter_message(text=ask, buttons=buttons)

        return []


class ActionRegularNursingRoundFlow(Action):

    def name(self) -> Text:
        return "action_regular_nursing_round_flow"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name, phone = get_name_phone(tracker)
        logger.info(f"{__file__} : Round : Nursing Round |  name : {name} | phone : {phone}")

        m1 = f"Good Morning {name}! How are you feeling today ?"

        ask = m1

        buttons = button_it(_feel_better_buttons())
        dispatcher.utter_message(text=ask, buttons=buttons)

        return []
