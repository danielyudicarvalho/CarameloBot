
from typing import Any, Text, Dict, List
from urllib import response
from numpy import extract
from pydantic import UrlSchemeError

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
import bs4
import urllib.request as urllib_request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient
from sklearn.feature_extraction import image


QUESTION = {
     "prevenção": "prevent",
     "tratamentos":"treatments",
     "sintomas":"symptoms" ,
     "sintoma":"symptoms",
     "prevenir":"prevent",
     "tratamento":"treatments",
     "tratar":"treatments"
 }


class ActionScrapping(Action):

    def name(self) -> Text:
        return "action_scrapping"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 

        size_slot = tracker.get_slot("size")
        age_slot = tracker.get_slot("age")
        animal_type_slot = tracker.get_slot("animal_type")
        gender_slot = tracker.get_slot("gender")
        urls = []

        cluster = MongoClient("mongodb+srv://danielyudi:elysium4@cluster0.catne.mongodb.net/mydatabase?retryWrites=true&w=majority")
        db = cluster["mydatabase"]
        mycol = db["pets"]
        pets = list(mycol.find({"goal":"Adocao","size":size_slot,"age":age_slot,"animal_type":animal_type_slot,"gender":gender_slot}))
     
        if len(pets)<3:
            index=0
            for pet in pets:
                index+=1
                dispatcher.utter_message(text=pet['link'])
                dispatcher.utter_message(text=pet['name'])
                dispatcher.utter_message(image=pet['photo'])
                dispatcher.utter_message(text=pet['phone'])
                dispatcher.utter_message(text=pet['email'])
            
        elif len(pets)>5:
            for i in range(0,2):
                dispatcher.utter_message(text=pets[i]['link'])
                dispatcher.utter_message(text=pets[i]['name'])
                dispatcher.utter_message(image=pets[i]['photo'])
                dispatcher.utter_message(text=pets[i]['phone'])
                dispatcher.utter_message(text=pets[i]['email'])
            
            dispatcher.utter_message(text="Acesse o site caso não tenha encontrado o que estava buscando")
            dispatcher.utter_message(text="https://adotar.com.br/busca.aspx?cc=1484&cn=ms-campo-grande")

        else:
            dispatcher.utter_message(text="Infelizmente não encontramos nenhum resultado para sua busca. Você pode fazer uma busca mais aprofundada nesse site:")
            dispatcher.utter_message(text="https://adotar.com.br/busca.aspx?cc=1484&cn=ms-campo-grande")
            

        
      
        urls =[]
        return [AllSlotsReset()]


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
 

        return [AllSlotsReset()]
