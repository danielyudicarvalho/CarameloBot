

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
        utter_response_prevent = 'utter_answer_initial_info_{disease}'.format(disease=disease_slot)
        utter_response_prevent = 'utter_answer_prevent_{disease}'.format(disease=disease_slot)
        utter_response_symptoms = 'utter_answer_symptoms_{disease}'.format(disease=disease_slot)
        utter_response_treatment = 'utter_answer_treatment_{disease}'.format(disease=disease_slot)
        utter_response_more_info = 'utter_answer_more_info_{disease}'.format(disease=disease_slot)
        dispatcher.utter_message(response=utter_response_prevent)
        dispatcher.utter_message(response=utter_response_symptoms)
        dispatcher.utter_message(response=utter_response_treatment)
        dispatcher.utter_message(response=utter_response_more_info)

        return []
