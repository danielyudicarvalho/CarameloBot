from cgitb import text
from typing import Any, Text, Dict, List
from urllib import response
from numpy import extract
from pydantic import UrlSchemeError
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy import null
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import SlotSet
import urllib.request as urllib_request
from urllib.request import urlopen
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

DISEASE=['leishmaniose','raiva','sarna','toxoplasmose']
#================================================================== 
# ActionSendEmail - implementa uma função para enviar email
# email personalizado
#==================================================================
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(name, email, phone, how_to_help):
    port = 587                                       # Porta na qual é feita a comunicação

    sender_email = "abrigo.do.bicho.bot@gmail.com"       # Email do Remetente
    password = "Abrigo@bicho"                            # Senha do Remetente
    receiver_email = "abrigo.do.bicho.bot@gmail.com"     # Email do Destinatário

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

    msg.attach(text)        # É possível colocar outros formatos ex: html, csv, etc
    msg = msg.as_string()   # Importante enviar no formato string

    s = smtplib.SMTP('smtp.gmail.com', port)
    s.starttls() 
    s.login(sender_email, password)
    s.sendmail(sender_email, receiver_email, msg)
    s.quit()

class ActionSendEmail(Action):

    def name(self) -> Text:
        return "action_send_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name_slot")
        email = tracker.get_slot("email_slot")
        phone = tracker.get_slot("contact_number_slot")
        how_to_help = tracker.get_slot("how_to_help_slot")
        
        reception_number = "" # Número da pessoa responsável por recepcionar o cliente
        reception_text = f"""
        Olá, meu nome é {name}, desejo me voluntariar, auxiliando com:
        {how_to_help}"""      # Texto receptivo
        reception_text = reception_text.replace(" ", "%20")

        send_email(name, email, phone, how_to_help)

        dispatcher.utter_message(text=f"""
        Obrigado pelas informações {name}, encaminhei um email para o abrigo com seus dados, clique no link abaixo para continuar a conversa com um humano :)\nhttps://api.whatsapp.com/send?phone={reception_number}&text={reception_text}
        """)

        return []
 

class ActionSendWhats(Action):

    def name(self) -> Text:
        return "action_send_whats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name_slot")
        what_to_donate = tracker.get_slot("what_to_donate_slot")

        reception_number = "" # Número da pessoa responsável por recepcionar o cliente
        reception_text = f"""
        Olá, meu nome é {name}, desejo ajudar doando:
        {what_to_donate}"""      # Texto receptivo
        reception_text = reception_text.replace(" ", "%20")

        dispatcher.utter_message(text=f"""
        Obrigado pelas informações {name}, clique no link abaixo para continuar a conversa com um humano :)\nhttps://api.whatsapp.com/send?phone={reception_number}&text={reception_text}
        """)

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
# ActionUtterGreet - implementa uma função para cumprimentar
# cumprimentos personalizados 
#==================================================================
class ActionUtterGreet(Action):

    def name(self) -> Text:
        return "action_utter_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # pega a ultima mensagem e alcança o nome publico do usuário no telegram
        input_data=tracker.latest_message
        user_name=input_data["metadata"]["message"]["from"]["first_name"]

        timezone = pytz.timezone('America/Campo_Grande')
        hoje = datetime.now(timezone)
        hora_atual = hoje.hour
        utter_bom_dia = "Oláá "+ user_name +" um bom dia! Como posso te ajudar?"

        utter_boa_tarde = "Oláá "+ user_name +" uma boa tarde! Como posso te ajudar?"

        utter_boa_noite = "Oláá "+ user_name +" uma boa noite! Como posso te ajudar?"    
        
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


class ActionResetHelpSlots(Action):

     def name(self) -> Text:
        return "action_reset_help_slots"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("email_slot", None), SlotSet("contact_number_slot", None), SlotSet("how_to_help_slot", None)]

class ActionResetPetSlots(Action):

     def name(self) -> Text:
        return "action_reset_all_slots"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("animal_type_slot", None), SlotSet("size", None), SlotSet("age", None), SlotSet("gender", None)]

class ActionResetNameSlot(Action):

     def name(self) -> Text:
        return "action_reset_name_slot"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("name_slot", None)]
