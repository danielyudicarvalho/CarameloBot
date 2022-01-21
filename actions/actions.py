from cgitb import text
from typing import Any, Text, Dict, List
from urllib import response
from numpy import extract
from pydantic import UrlSchemeError
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
import urllib.request as urllib_request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

AGE = ('Abaixo-de-2-meses','2-a-6-meses','7-a-11-meses','1-ano','2-anos','3-anos','4-anos','5-anos','6-anos-Acima')
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
            urls = ['https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE[0],porte=size_slot,sexo=gender_slot),
                    'https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE[1],porte=size_slot,sexo=gender_slot)]
        elif age_slot == 'children':
            urls = ['https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE[2],porte=size_slot,sexo=gender_slot),
                    'https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=AGE[3],porte=size_slot,sexo=gender_slot)]
        else:
            for i in AGE[4:]:
                urls.append('https://adotar.com.br/animais.aspx?cc=1484&cn=ms-campo-grande&finalidade=Adocao&tipo={tipo}&porte={porte}&idade={idade}&sexo={sexo}'.format(tipo=animal_type_slot,idade=i,porte=size_slot,sexo=gender_slot))

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

        urls =[]
        return [AllSlotsReset()]

#================================================================== 
# ActionSubmit - implementa uma função para enviar email
# email personalizado
#==================================================================


def send_email(name, email, phone, how_to_help):
    port = 587
    sender_email = "testpythontoday@gmail.com"
    receiver_email = "testpythontoday@gmail.com"
    password = "testpython3@" 

    text = f"""
    Mais um voluntário para a causa :)

    Nome: {name}
    Email: {email}
    Telefone: {phone}
    Descrição: {how_to_help}
    """
    text = MIMEText(text, 'plain')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Voluntário - Abrigo dos Bichos"

    msg.attach(text)        # É possível colocar outros formatos
    msg = msg.as_string()   # Importante enviar no formato string

    s = smtplib.SMTP('smtp.gmail.com', port)
    s.starttls() 
    s.login(sender_email, password)
    s.sendmail(sender_email, receiver_email, msg)
    s.quit()

class ActionSubmit(Action):

    def name(self) -> Text:
        return "action_send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name_slot")
        email = tracker.get_slot("email_slot")
        phone = tracker.get_slot("contact_number_slot")
        how_to_help = tracker.get_slot("how_to_help_slot")

        send_email(name, email, phone, how_to_help)
        dispatcher.utter_message(text=f"Email enviado com sucesso!")

        return []
#================================================================== 
# ActionUtterGreet - implementa uma função para cumprimentar
# cumprimentos personalizados 
#==================================================================


timezone = pytz.timezone('America/Campo_Grande')
hoje = datetime.now(timezone)
hora_atual = hoje.hour

utter_bom_dia = "Bom dia! Meu nome é Caramelo, eu e o Abrigo dos Bichos  vamos ajudá-lo(a) a solucionar suas dúvidas."

utter_boa_tarde = "Boa tarde! Meu nome é Caramelo, eu e o Abrigo dos Bichos  vamos ajudá-lo(a) a solucionar suas dúvidas."

utter_boa_noite = "Boa noite! Meu nome é Caramelo, eu e o Abrigo dos Bichos  vamos ajudá-lo(a) a solucionar suas dúvidas."

class ActionUtterGreet(Action):

    def name(self) -> Text:
        return "action_utter_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if hora_atual < 12:
            dispatcher.utter_message(text=utter_bom_dia)
        elif hora_atual < 19:
            dispatcher.utter_message(text=utter_boa_tarde)
        else:
            dispatcher.utter_message(text=utter_boa_noite)

        return []
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
      