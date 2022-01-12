

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

QUESTION = {
     "prevenção": "prevent",
     "tratamentos":"treatments",
     "sintomas":"symptoms" ,
     "sintoma":"symptoms",
     "prevenir":"prevent",
     "tratamento":"treatments"
 }

DISEASE=['leishmaniose','raiva','sarna','toxoplasmose']

class ActionAnswerDisease(Action):

    def name(self) -> Text:
        return "action_answer_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease_slot = tracker.get_slot("disease")
        question_slot = tracker.get_slot("question")

        if QUESTION[question_slot]:
            utter_response_answer = 'utter_answer_{question}_{disease}'.format(disease=disease_slot,question=QUESTION[question_slot])
        else:
            utter_response_answer = 'utter_answer_initial_info_{disease}'.format(disease=disease_slot)
        
        print(utter_response_answer)
        print(QUESTION[question_slot])
        dispatcher.utter_message(response=utter_response_answer)
 

        return []

class ActionAnswerDiseaseSymptoms(Action):

    def name(self) -> Text:
        return "action_answer_disease_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease_slot = tracker.get_slot("disease")
        utter_response_symptoms = 'utter_answer_symptoms_{disease}'.format(disease=disease_slot)
        dispatcher.utter_message(response=utter_response_symptoms)
 

        return []
class ActionAnswerDiseasePrevent(Action):

    def name(self) -> Text:
        return "action_answer_disease_prevent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        disease_slot = tracker.get_slot("disease")
        
        utter_response_prevent = 'utter_answer_prevent_{disease}'.format(disease=disease_slot)
        dispatcher.utter_message(response=utter_response_prevent)

 

        return []

class ActionAnswerDiseaseTreatment(Action):

    def name(self) -> Text:
        return "action_answer_disease_treatment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease_slot = tracker.get_slot("disease")   
        utter_response_treatment = 'utter_answer_treatment_{disease}'.format(disease=disease_slot)
        dispatcher.utter_message(response=utter_response_treatment)

        return []