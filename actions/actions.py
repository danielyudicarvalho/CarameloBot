# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


QUESTION = {
     "prevenção": "prevent",
     "tratamentos":"treatments",
     "sintomas":"symptoms" ,
     "sintoma":"symptoms",
     "prevenir":"prevent",
     "tratamento":"treatments",
     "tratar":"treatments"
 }

DISEASE=['leishmaniose','raiva','sarna','toxoplasmose']

#================================================================== 
# ActionAnswerDisease - implementa uma função para falar  
# sobre as zoonoses
#==================================================================
class ActionAnswerDisease(Action):

    def name(self) -> Text:
        return "action_answer_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        disease_slot = tracker.get_slot("disease")
        question_slot = tracker.get_slot("question")

        if question_slot and QUESTION[question_slot]:
            utter_response_answer = 'utter_askaction/ask_{question}_{disease}'.format(disease=disease_slot,question=QUESTION[question_slot])
        else:
            utter_response_answer = 'utter_askaction/ask_initial_info_{disease}'.format(disease=disease_slot)
        
        
        dispatcher.utter_message(response=utter_response_answer)
 

        return []
#================================================================== 
# ActionAnswerDiseaseSymptoms - implementa uma função para falar  
# sobre os sintomas das zoonoses
#==================================================================
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
#================================================================== 
# ActionAnswerDiseasePrevent - implementa uma função para falar  
# sobre a prevenção das zoonoses
#==================================================================

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

#================================================================== 
# ActionAnswerDiseaseTreatment - implementa uma função para falar  
# sobre o tratamento das zoonoses
#==================================================================
      
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
      
#================================================================== 
# Action about vaccine - implementa uma função para falar sobre 
# as vacinas
#==================================================================
      
class ActionAboutVaccine(Action):

    def name(self) -> Text:
        return "action_about_vaccine"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Entrei na vacina!")

        return []

