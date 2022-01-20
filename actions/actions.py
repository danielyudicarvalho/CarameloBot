
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
AGE = {
     "ageOne": "Abaixo-de-2-meses",
     "ageTwo":"2-a-6-meses",
     "ageThree":"7-a-11-meses" ,
     "ageFour":"1-ano",
     "ageFive":"2-anos",
     "ageSix":"3-anos",
     "ageSeven":"4-anos",
     "ageEight":"5-anos",
     "ageNine":"6-anos-Acima",
 }

AGE3 = ('Abaixo-de-2-meses','2-a-6-meses','7-a-11-meses','1-ano','2-anos','3-anos','4-anos','5-anos','6-anos-Acima')

# async def extractOne(url):
#     response = urlopen(url)
#     html = response.read()
#     soup = BeautifulSoup(html, 'html.parser')
#     res = soup.findAll('div', class_="listaAnimais")
#     return res

async def extractTwo(url):
    responseLink = urlopen(url)
    htmlLink = responseLink.read()
    soupLink = BeautifulSoup(htmlLink, 'html.parser')
    return soupLink

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
        
        if age_slot == 'baby':
            urls = ['https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE3[0],porte=size_slot,sexo=gender_slot),
                    'https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE3[1],porte=size_slot,sexo=gender_slot)]
        elif age_slot == 'children':
            urls = ['https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE3[2],porte=size_slot,sexo=gender_slot),
                    'https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE3[3],porte=size_slot,sexo=gender_slot)]
        else:
            for i in AGE3[4:]:
                urls.append('https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=i,porte=size_slot,sexo=gender_slot))

        #url_response = 'https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE2[1],porte=size_slot,sexo=gender_slot)
        print(urls)

        for i in urls:
            response = urlopen(i)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            res = soup.findAll('div', class_="listaAnimais")
            print(len(res))
            if len(res)>0:
                for item in res:
                    link = item.find('a')['href']
                    link = 'https://adotar.com.br'+link
                    print(link)
                    dispatcher.utter_message(text=link)
                    photo = 'https://'+item.find('img')['src'][2:]
                    print(photo)
                    dispatcher.utter_message(image=photo)
                    name = item.find('div',{'class':'listaAnimaisDados'})
                    name = name.get_text().split()
                    print(name[0])
                    dispatcher.utter_message(text=name[0])

            # responseLink = urlopen(link)
            # htmlLink = responseLink.read()
            # soupLink = BeautifulSoup(htmlLink, 'html.parser')

            #soupLink = await extractTwo(link)
            #contact = soupLink.find('a',{"id":"mailprop"})
            # email = contact['href']
            # phone = contact.findNextSibling().find('a').getText()
            # print(str(email[7:]))
            # print(str(phone))
            # dispatcher.utter_message(text='email: {mail}'.format(mail=email[6:]))
            # dispatcher.utter_message(text='telefone: {telefone}'.format(telefone=phone))
        
            

        
      
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