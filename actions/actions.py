# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from db.mongo import Person
import sys
sys.path.append("../")
import logging
from typing import Any, Text, Dict, List, Optional, Tuple

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet
from datetime import datetime as dt, time
from utils.helper import *
from utils import diginurse_utils as dg


name = "Hemanth"
phone = 7989898989
def yes_no():
    return [
        ("Yes", "Yes"),
        ("No", "No")
    ]


class FetchRound(Action):

    def name(self) -> Text:
        return "action_round"

    def getRound(self, name,  phone):
        if dg.checkScheduleNoSet(name, phone):
            return 'configure'
        else:
            return 'new_treatment'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender = tracker.sender_id

        # round = Person(sender).load_round(sender)
        # Irfan
        # load round field from db
        round = self.getRound(name, phone)

        if round != -1:
            logger.info(f"{__file__} :  Found round ****************** : {round}")
        else:
            logger.info(f"{__file__} :  No sender found with {sender} ******************")

        return [SlotSet("round", round)]


class ActionComebackLater(Action):

    def name(self) -> Text:
        return "action_comeback_later"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tell = "Please come back when you have few minutes on your hand"
        dispatcher.utter_message(text=tell)

        return []


class ActionImproveExperience(Action):

    def name(self) -> Text:
        return "action_improve_experience"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        sender = tracker.sender_id
        for each in tracker.events:
            logger.info(f"{__file__} : each : {each}")
        
        logger.info(f"{__file__} : sender_id : {sender}")

        p = dg.getPatient(name,phone)
        print(p)
        
        op = [("Yes you have", "Yes you have my consent"), ("No you dont", "no you dont have my consent")]
        buttons = button_it(op)
        ask = "Do we have your consent to use this  information to improve your experience ?"

        dispatcher.utter_message(text=ask,buttons=buttons)

        return []


class SleepTimeForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_sleep_time"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["sleep_time","wakeup_time"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity"""
        return {
                "sleep_time": self.from_text(),
                "wakeup_time": self.from_text()
                }

    def _wakeup_times(self):
        return [
            "7:00-8:00 ",
            "8:00-9:00 ",
            "9:00-10:00 ",
            "10:00-11:00",
        ]

    def _sleep_times(self):
        return [
            "20:00-21:00 ",
            "21:00-22:00 ",
            "22:00-23:00 ",
            "23:00-00:00 ",
        ]

    def request_next_slot(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Optional[List[Dict]]:
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                # utter template and request slot
                if slot == "sleep_time":
                    buttons = self._sleep_times()
                    buttons = button_it(buttons)
                    ask = "First we will cover your sleep timings <br><strong class=\"imp\"> When do you go to bed everyday ? </strong>"
                    dispatcher.utter_message(text=ask, buttons=buttons)
                elif slot == "wakeup_time":
                    buttons = self._wakeup_times()
                    buttons = button_it(buttons)

                    ask = "When do you wake up in the morning ?"
                    dispatcher.utter_message(text=ask, buttons=buttons)
                return [SlotSet("requested_slot", slot)]
        return None

    def validate_sleep_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate sleep_time value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} :  : text : {value} | intent : {intent}")
        if intent == "times":
            # Irfan
            # update sleep time field in db
            dg.updateSchedule(name, phone, bed_time=value)

            return {"sleep_time": value}
        else:
            return {"sleep_time": None}

    def validate_wakeup_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate wakeup_time value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} :  : text : {value} | intent : {intent}")
        if intent == "times":
            # Irfan
            # update wake time field in db
            dg.updateSchedule(name, phone, wakeup_time=value)
            return {"wakeup_time": value}
        else:
            return {"wakeup_time": None}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        sleep_time = tracker.get_slot('sleep_time')
        wakeup_time = tracker.get_slot('wakeup_time')
        tell = f"Great! I'll remember that you sleep at {sleep_time} and wake up at {wakeup_time}"
        tell += "\n Next is your meal timings"
        dispatcher.utter_message(text=tell)
        return []


class MealTimeForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_meal_time"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["breakfast_time","lunch_time","dinner_time"]
    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity"""
        
        return {"breakfast_time": self.from_text(),
                "lunch_time": self.from_text(),
                "dinner_time": self.from_text()
                }
    def _breakfast_times(self):
        wakeup_time = self.tracker.get_slot('wakeup_time')
        entities = self.tracker.latest_message['entities']
        logger.info(f"{__file__} : entities : {entities}")
        for entity in entities:
            if entity['entity'] == 'time':
                wakeup_time = entity['value']
                if len(wakeup_time) <= 2:
                    wakeup_time = wakeup_time + ":00"
                break
        logger.info(f"{__file__} : wakeup_time : {wakeup_time}")
        limit = 12
        
        # break_fast_times = get_time_diff(wakeup_time,limit,context="breakfast")

        break_fast_times = [
            "7:00-8:00 ",
            "8:00-9:00 ",
            "9:00-10:00 ",
            "10:00-11:00 ",
        ]

        logger.info(f"{__file__} : break_fast_times : {break_fast_times}")
        return break_fast_times

    def _lunch_times(self):
        break_fast_time = self.tracker.get_slot('breakfast_time')

        entities = self.tracker.latest_message['entities']
        logger.info(f"{__file__} : entities : {entities}")
        for entity in entities:
            if entity['entity'] == 'time':
                break_fast_time = entity['value']
                if len(break_fast_time) <= 2:
                    break_fast_time = break_fast_time + ":00"

                break
        limit = 4
        # lunch_times = get_time_diff(break_fast_time,limit,context="lunch")

        lunch_times = [
            "12:00-13:00 ",
            "13:00-14:00 ",
            "14:00-15:00 ",
        ]
        logger.info(f"{__file__} : lunch_times : {lunch_times}")

        return lunch_times
    def _dinner_times(self):
        lunch_time = "4:00"
        entities = self.tracker.latest_message['entities']
        logger.info(f"{__file__} : entities : {entities}")
        # for entity in entities:
        #     if entity['entity'] == 'time':
        #         lunch_time = entity['value']
        limit = 11
        # dinner_times = get_time_diff(lunch_time,limit,context="dinner")

        dinner_times = [
            "19:00-20:00 ",
            "21:00-22:00 ",
            "22:00-23:00 ",
        ]
        logger.info(f"{__file__} : dinner_times : {dinner_times}")

        return dinner_times

    def request_next_slot(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Optional[List[Dict]]:
        """Request the next slot and utter template if needed,
            else return None"""
        till_now = [{i:tracker.get_slot(i)} for i in self.required_slots(tracker)]
        logger.info(f"{__file__} : till now : {till_now}")
        self.tracker = tracker
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                # utter template and request slot
                
                if slot == "breakfast_time":
                    buttons = self._breakfast_times()
                    buttons = button_it(buttons)

                    ask = "<strong class=\"imp\">When do you generally have your breakfast?</strong>"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                elif slot == "lunch_time":
                    buttons = self._lunch_times()
                    buttons = button_it(buttons)

                    ask = "At what time you have your lunch?"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                elif slot == "dinner_time":
                    buttons = self._dinner_times()
                    buttons = button_it(buttons)
                    ask = "Finally, when do you generally have your dinner?"
                    dispatcher.utter_message(text=ask,buttons=buttons)

                return [SlotSet("requested_slot", slot)]
        return None

    def validate_breakfast_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
        """Validate breakfast_time value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "times":
            # Irfan 
            # update breakfast time field in db
            dg.updateSchedule(name, phone, breakfast_time=value)
            return {"breakfast_time": value}
        else:
            return {"breakfast_time": None}
    def validate_lunch_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
        """Validate lunch_time value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "times":
            # Irfan 
            # update lunch time field in db
            dg.updateSchedule(name, phone, lunch_time=value)

            return {"lunch_time": value}
        else:
            return {"lunch_time": None}
    def validate_dinner_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:
        """Validate dinner_time value."""
        intent = tracker.latest_message['intent'].get('name')
        if intent == "times":
            # Irfan 
            # update dinner time field in db
            dg.updateSchedule(name, phone, dinner_time=value)

            return {"dinner_time": value}
        else:
            return {"dinner_time": None}
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        breakfast_time = tracker.get_slot('breakfast_time')
        lunch_time = tracker.get_slot('lunch_time')
        dinner_time = tracker.get_slot('dinner_time')
        tell = f"Great! I'll remember that you eat at {breakfast_time} and {lunch_time} and {dinner_time}"
        
        
        dispatcher.utter_message(text=tell)
        return []


class AskSmokeForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_ask_smoke"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["smoking","smoke_freq"]
    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity"""
        
        return {"smoking": self.from_text(),
                "smoke_freq": self.from_text()
                }

    def _smoke_freq(self):
        return [
            ("Daily", "Daily"),
            ("Frequently", "Frequently"),
            ("Occasionally", "Occasionally")
        ]
    def _yes_no(self):
        return [
            ("Yes", "Yes"),
            ("No", "No")
        ]
        
    def request_next_slot(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Optional[List[Dict]]:
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                # utter template and request slot
                if slot == "smoking":
                    buttons = self._yes_no()
                    buttons = button_it(buttons)
                    ask = "<br><strong class=\"imp\">Do you smoke?</strong>"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                elif slot == "smoke_freq":
                    buttons = self._smoke_freq()
                    buttons = button_it(buttons)

                    ask = "How often do you smoke?"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                return [SlotSet("requested_slot", slot)]
        return None

    def validate_smoking(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate smoking value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "affirm":
            # Irfan 
            # update smoking time field in db
            dg.updateSchedule(name, phone, smoke=value)

            return {"smoking": value}
        else:
            dg.updateSchedule(name, phone, smoke="No")
            return {"smoking": "No", "smoke_freq": "No"}
    def validate_smoke_freq(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate smoke_freq value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "how_often":
            # Irfan 
            # update smoke time field in db
            dg.updateSchedule(name, phone, smoke=value)

            return {"smoke_freq": value}
        else:
            return {"smoke_freq": None}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        
        smoking = tracker.get_slot('smoking')
        smoke_freq = tracker.get_slot('smoke_freq')
        logger.info(f"{__file__} : smoking : {smoking} | smoke_freq : {smoke_freq}")
        return []
        

class AskDrinkForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_ask_drink"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["drinking","drink_freq"]
    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity"""
        
        return {"drinking": self.from_text(),
                "drink_freq": self.from_text(),
                }

    def _drink_freq(self):
        return [
            ("Daily", "Daily"),
            ("Frequently", "Frequently"),
            ("Occasionally", "Occasionally")
        ]
    def _yes_no(self):
        return [
            ("Yes", "Yes"),
            ("No", "No")
        ]
        
    def request_next_slot(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Optional[List[Dict]]:
        """Request the next slot and utter template if needed,
            else return None"""

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                # utter template and request slot
                if slot == "drinking":
                    buttons = self._yes_no()
                    buttons = button_it(buttons)
                    ask = "Do you drink alcohol?"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                elif slot == "drink_freq":
                    buttons = self._drink_freq()
                    buttons = button_it(buttons)

                    ask = "How often do you drink alcohol?"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                return [SlotSet("requested_slot", slot)]
        return None

    def validate_drinking(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate drinking value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "affirm":
            # Irfan 
            # update drinking time field in db
            dg.updateSchedule(name, phone, drink=value)

            return {"drinking": value}
        else:
            dg.updateSchedule(name, phone, drink="No")
            return {"drinking": "No", "drink_freq": "No"}
    def validate_drink_freq(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate drink_freq value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "how_often":
            # Irfan 
            # update drink time field in db
            dg.updateSchedule(name, phone, drink=value)

            return {"drink_freq": value}
        else:
            return {"drink_freq": None}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        
        drinking = tracker.get_slot('drinking')
        drink_freq = tracker.get_slot('drink_freq')
        logger.info(f"{__file__} : drinking : {drinking} | drink_freq : {drink_freq}")
        return []
        

class AskWorkOutForm(FormAction):
    """Example of a custom form action"""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_ask_workout"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["workingout","workout_freq","intence"]
    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity"""
        
        return {"workingout": self.from_text(),
                "workout_freq": self.from_text(),
                "intence":self.from_text()
                }

    def _workout_freq(self):
        return [
            ("Daily", "Daily"),
            ("Frequently", "Frequently"),
            ("Occasionally", "Occasionally")
        ]
    def _how_intence(self):
        return [
            ("Low", "low"),
            ("Medium", "medium"),
            ("High", "high")
        ]

    def _yes_no(self):
        return [
            ("Yes", "Yes"),
            ("No", "No")
        ]
        
    def request_next_slot(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Optional[List[Dict]]:
        """Request the next slot and utter template if needed,
            else return None"""
        till_now = [{i:tracker.get_slot(i)} for i in self.required_slots(tracker)]
        logger.info(f"{__file__} : till now : {till_now}")
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                # utter template and request slot
                if slot == "workingout":
                    buttons = self._yes_no()
                    buttons = button_it(buttons)
                    ask = "Do you workout?"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                elif slot == "workout_freq":
                    buttons = self._workout_freq()
                    buttons = button_it(buttons)

                    ask = "How often do you workout ?"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                elif slot == "intence":
                    buttons = self._how_intence()
                    buttons = button_it(buttons)

                    ask = "How intence is your workout session ?"
                    dispatcher.utter_message(text=ask,buttons=buttons)
                return [SlotSet("requested_slot", slot)]
        return None

    def validate_workingout(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate workingout value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "affirm":
            # Irfan 
            # update workout time field in db
            dg.updateSchedule(name, phone, workout=value)

            return {"workingout": value}
        else:
            logger.info("Workout No")
            dg.updateSchedule(name, phone, workout="No")
            return {"workingout": "No", "workout_freq": "No","intence":"No"}

    def validate_workout_freq(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate workout_freq value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "how_often":
            # Irfan 
            # update how_often workout field in db
            dg.updateSchedule(name, phone, workout=value)

            return {"workout_freq": value}
        else:
            return {"workout_freq": None}

    def validate_intence(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate intence value."""
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "how_intense":
            # Irfan 
            # update intence [low,high,medium] field in db
            dg.updateSchedule(name, phone, workout=value)

            return {"intence": value}
        else:
            return {"intence": None}



    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        
        workingout = tracker.get_slot('workingout')
        workout_freq = tracker.get_slot('workout_freq')
        intence = tracker.get_slot('intence')
        logger.info(f"{__file__} : workingout : {workingout} | workout_freq : {workout_freq} | intence : {intence}")
        tell = dg.showSchedule(name, phone)
        tell += "\nAwesome! Your diginurse is configured and ready to go. Let's start working to feel you better"
        tell += "\nYou can update the changes in your routine and life style just by chatting with me \n\n<strong class=\"imp\">. \nFor example, just type Change my breakfast time </strong>"
        dispatcher.utter_message(text=tell)
        return []
       
       
class ActionThankYou(Action):

    def name(self) -> Text:
        return "action_thank_you"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        ask = "Thank you message"
        dispatcher.utter_message(text=ask)
        return []


class ActionConfigured(Action):

    def name(self) -> Text:
        return "action_configured"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        tell = "Awesome! Your Diginurse is configured and ready to go. Let's start working to feel you better."
        tell += "You can update the changes in your routine and life style just by chating with me \n\n For example, just type ' Change my breakfast time '"
        dispatcher.utter_message(text=tell)
        return []


class ActionRecommend(Action):

    def name(self) -> Text:
        return "action_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        logger.info(f"{__file__} : Inside action recommend")
        tell = "\nBased on your routine I recommend you following timings for your regular nursing rounds"
        tell += "\n"+dg.showNursingRounds(name, phone)
        tell += "\n\nDo you want to change timings of any followup ?"

        buttons = yes_no()
        buttons = button_it(buttons)

        dispatcher.utter_message(text=tell, buttons=buttons)

        return []


class ActionRecommenddeny(Action):

    def name(self) -> Text:
        return "action_deny_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tell = "Perfect! Everything is set for your recovery. Quote"
        dispatcher.utter_message(text=tell)

        return []


class ActionAskChages(Action):

    def name(self) -> Text:
        return "action_ask_changes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tell = "Please type the task timings or lifestyle activity you want to change."
        tell += 'For example, type <strong class="imp"> Change my breakfast time </strong>'
        dispatcher.utter_message(text=tell)
        return []


class FormChanges(FormAction):
    """Example of a custom form action"""
    _time_clash = 0   # TODO :: create a enum as None , Clashing and Not-Clashing

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "form_changes"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["change_field", "time", "loop"]

    def slot_mappings(self):
        """A dictionary to map required slots to
            - an extracted entity"""
        
        return {
                "change_field": self.from_text(),
                "time": self.from_text(),
                "loop": self.from_text()
                }
    
    def _yes_no(self):
        return [
            ("Yes", "Yes"),
            ("No", "No")
        ]
        
    def request_next_slot(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> Optional[List[Dict]]:
        """Request the next slot and utter template if needed,
            else return None"""
        logger.info(f"{__file__} : Inside request_next_slot of FormChanges")

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):

                # utter template and request slot
                if slot == "change_field":
                    tell = "Please type the task timings or lifestyle activity you want to change."
                    tell += 'For example, type <strong class="imp"> Change my breakfast time </strong>'

                    dispatcher.utter_message(text=tell)

                elif slot == "time":
                    if self._time_clash == 1:
                        ask = f"\nThere is a clash with {self._time_clash} timing in your schedule."
                        ask += "\n\nPlease enter non conflicting time again."
                        dispatcher.utter_message(text=ask)
                    else:
                        field = tracker.get_slot("change_field")
                        ask = f"\nWhat is your updated {field} time ?"
                        dispatcher.utter_message(text=ask)
                elif slot == "loop":
                    tell = "\nYour routine has been updated."
                    ask = tell + dg.showNursingRounds(name, phone)
                    dispatcher.utter_message(text=ask)

                    ask = "\n Do you want to change timings of any followup ?"
                    buttons = yes_no()
                    buttons = button_it(buttons)
                    dispatcher.utter_message(text=ask, buttons=buttons)

                return [SlotSet("requested_slot", slot)]
        return None

    def validate_change_field(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate change_field value."""
        logger.info(f"{__file__} : Inside validate change field")
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")
        if intent == "change_time":
            field = tracker.get_slot("routines")
            time  = tracker.get_slot("time")

            logger.info(f"{__file__} : End of validate change field | change field = {field} , time = {time} ")
            return {"change_field": field, "time": time}
        else:
            logger.info(f"{__file__} : End of validate change field | change_filed = None ")
            return {"change_field": None}

    def validate_time(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate time value."""
        logger.info(f"{__file__} : Inside validate time")
        intent = tracker.latest_message['intent'].get('name')
        logger.info(f"{__file__} : text : {value} | intent : {intent}")

        if intent in ["times", "change_time"]:
            field = tracker.get_slot("routines")
            timing = tracker.get_slot("time")
            ret = 'No'
            # Irfan
            # check for clashes and update the time
            #  and return a name of the class timinig
            if field is not None:
                ret = dg.checkTimeOverlap(name, phone, field, timing)

            if ret is not None and ret != 'No':
                logger.info(f"{__file__} : There is an overlap with {ret} timings")
                # There is an overlap, print a message
                self._time_clash = 1   # TODO ::  Clashing
                return {"time": None}
            else:
                logger.info(f"{__file__} : There is NO overlap with any timings, ret = {ret}")
                # There is no overlap
                self._time_clash = 0   # TODO :: Not-Clashing
                dg.updateSchedule(name, phone,  kargs={f"{field}_time": timing})
                return {"time": str(timing)}
        else:
            logger.info(f"{__file__} : End of validate time")
            return {"time": None}

    def validate_loop(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        logger.info(f"{__file__} : Inside submit validate_loop")
        
        intent = tracker.latest_message['intent'].get('name')
        if intent == "affirm":
            return {"change_field": None, "time": None, "loop": None}
        else:
            return {"loop": "no"}

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        logger.info(f"{__file__} :  Inside submit formchanges")
        field = tracker.get_slot('change_field')
        time = tracker.get_slot('time')
        tell = f"Your routine has been updated"
        
        dispatcher.utter_message(text=tell)
        # dispatcher.utter_template('action_recommend', tracker)
        return []
 






























