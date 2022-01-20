# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from cgitb import text
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
# ActionSendEmail - implementa uma função para enviar email
# email personalizado
#==================================================================
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(name, email, phone, how_to_help):
    port = 587                                       # Porta na qual é feita a comunicação

    sender_email = "testpythontoday@gmail.com"       # Email do Remetente
    password = "testpython3@"                        # Senha do Remetente
    receiver_email = "testpythontoday@gmail.com"     # Email do Destinatário

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
#================================================================== 
# ActionUtterGreet - implementa uma função para cumprimentar
# cumprimentos personalizados 
#==================================================================
from datetime import datetime
import pytz

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

