
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

        url_response = 'https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE[age_slot],porte=size_slot,sexo=gender_slot)
        print(url_response)
        response = urlopen(url_response)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        res = soup.findAll('div', class_="listaAnimais")
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

            # soupLink = await extractTwo(link)
            # contact = soupLink.find('a',{"id":"mailprop"})
            # email = contact['href']
            # phone = contact.findNextSibling().find('a').getText()
            # print(str(email))
            # print(str(phone))
            # dispatcher.utter_message(text=email)
            # dispatcher.utter_message(text=phone)
        
            

        
        dispatcher.utter_message(text="Hello World!")

        return [AllSlotsReset()]
