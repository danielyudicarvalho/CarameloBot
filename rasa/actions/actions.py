

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

DISEASE = {
    'leishmaniose'
}

class ActionAnswerDisease(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease_slot = tracker.get_slot("disease")
        utter_response = 'utter_answer_{disease}'.format(disease=disease_slot)
        dispatcher.utter_message(response=utter_response)

        return []
