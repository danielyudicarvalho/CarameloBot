from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime
import pytz
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient
from .secrets import secrets
#================================================================== 
# ActionUtterGreet - implementa uma função para fazer
# cumprimentos personalizados 
#==================================================================
class ActionUtterGreet(Action):

    def name(self) -> Text:
        return "action_utter_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Pega a última mensagem e alcança o nome público do usuário no telegram
        name = tracker.get_slot("name_slot")
        if not name:
            # name = 'Filipe' # caso queira treinar no CLI, tirar essa linha do comentário e colocar as duas abaixo em comentário
            input_data=tracker.latest_message
            name = input_data["metadata"]["message"]["from"]["first_name"]
        # Como o escopo dos usuários é limitado a campo grande, o horario de comparação fica o de lá
        timezone = pytz.timezone('America/Campo_Grande')
        hoje = datetime.now(timezone)
        hora_atual = hoje.hour

        # Mensagens para serem usadas no utterance
        utter_boa_madrugada = "Olá "+ name +" uma boa madrugada! Como posso ajudá-lo? 😁" 

        utter_bom_dia = "Olá "+ name +" bom dia! Como posso ajudá-lo? 😁"

        utter_boa_tarde = "Olá "+ name +" boa tarde! Como posso ajudá-lo? 😁"

        utter_boa_noite = "Olá "+ name +" boa noite! Como posso ajudá-lo? 😁"    

        # Verificação para cada tipo de mensagem
        if hora_atual < 5 :
            dispatcher.utter_message(text=utter_boa_madrugada)
        if hora_atual < 12:
            dispatcher.utter_message(text=utter_bom_dia)
        elif hora_atual < 18:
            dispatcher.utter_message(text=utter_boa_tarde)
        elif hora_atual < 24:
            dispatcher.utter_message(text=utter_boa_noite)

        return [SlotSet("name_slot", name)]

#================================================================== 
# ActionSendEmail - implementa uma função para enviar email
# email personalizado
#==================================================================

def send_email(name, email, phone, how_to_help):
    port = 587                                       # Porta na qual é feita a comunicação

    sender_email = secrets['BOT_EMAIL']       # Email do Remetente
    password = secrets['BOT_EMAIL_PASSWORD']           # Senha do Remetente
    receiver_email = secrets['EMAIL_ABRIGO']     # Email do Destinatário / trocar para abrigodosbichos@abrigodosbichos.com.br após apresentações
    
    # Escopo da mensagem a ser enviada
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
        # pega os slots que irão compor a mensagem 
        name = tracker.get_slot("name_slot")
        email = tracker.get_slot("email_slot")
        phone = tracker.get_slot("contact_number_slot")
        how_to_help = tracker.get_slot("how_to_help_slot")

        # Função responsável por enviar o email
        send_email(name, email, phone, how_to_help)
        dispatcher.utter_message(text=f"Obrigado pelas informações {name}, encaminhei um email para o abrigo com seus dados!")
        return []
 
#================================================================== 
# ActionSendWhats - implementa uma função para enviar um link
# personalizado do whats para o usuário que quer doar
#==================================================================
class ActionSendWhats(Action):

    def name(self) -> Text:
        return "action_send_whats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # pega os slots que irão compor a mensagem
        name = tracker.get_slot("name_slot")
        what_to_donate = tracker.get_slot("what_to_donate_slot")
        
        # normalização da mensagem para o link do whats
        reception_number = secrets['WHATSAPP'] # Número da pessoa responsável por recepcionar o cliente
        reception_text = f"Olá, meu nome é {name}, desejo ajudar doando: {what_to_donate}"  # Texto receptivo
        reception_text = reception_text.replace(" ", "%20")
        link_whats = f"https://api.whatsapp.com/send?phone={reception_number}&text={reception_text}"
        
        # utterance do whats
        dispatcher.utter_message(text=f"Obrigado pelas informações {name}, clique no link abaixo para continuar a conversa com um humano :)\n")
        dispatcher.utter_message(text=f"{link_whats}")
        
        return []
#================================================================== 
# ActionSrapping - implementa uma função para enviar email
# email personalizado
#==================================================================
class ActionScrapping(Action):
    def name(self) -> Text:
        return "action_scrapping"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        
        # pega os slots que irão compor a busca no banco de dados
        size_slot = tracker.get_slot("size_slot")
        age_slot = tracker.get_slot("age_slot")
        animal_type_slot = tracker.get_slot("animal_type_slot")
        gender_slot = tracker.get_slot("gender_slot")
        
        # Normalização do animal do slot para fazer a busca no db
        dog = ['cão','cachorro', 'Cão', 'caozinho','cadela', 'cachorra','cachorinho', 'Cachorro',"Cao",'Cadela','Cachorra','Caos','Cachorros','Cães']
        cat = ['Gato','Gata', 'gatos','gatas','Gatos','Gatas','gatinhos','gatinhas','gatinha','gatinho','gato','gata']

        if animal_type_slot in dog:
            animal_type_slot = 'Cao'
        elif animal_type_slot in cat:
            animal_type_slot = 'Gato'
        # Acesso ao bd 
        cluster = MongoClient(secrets['MONGO_DB'])
        db = cluster["mydatabase"]
        mycol = db["pets"]
        # busca pela lista com as informações dos slots
        pets = list(mycol.find({"goal":"Adocao","size":size_slot,"age":age_slot,"animal_type":animal_type_slot,"gender":gender_slot}))
        # lógica dos utters baseado na quantidade de pets encontrados
        if 0 < len(pets) <= 3 :
            for pet in pets:
                dispatcher.utter_message(text='nome do pet: '+pet['name'])
                dispatcher.utter_message(image=pet['photo'])
                dispatcher.utter_message(text='LINK PARA ADOÇÃO: '+pet['link'])
                dispatcher.utter_message(text='telefone para contato: '+pet['phone'])
                dispatcher.utter_message(text='email para contato: '+pet['email'][7:])

        elif len(pets) > 3:
            for i in range(0,3):
                dispatcher.utter_message(text='nome do pet: '+pets[i]['name'])
                dispatcher.utter_message(image=pets[i]['photo'])
                dispatcher.utter_message(text='LINK PARA ADOÇÃO: '+pets[i]['link'])
                dispatcher.utter_message(text='telefone para contato: '+pets[i]['phone'])
                dispatcher.utter_message(text='email para contato: '+pets[i]['email'][7:])
            dispatcher.utter_message(text="Existem mais opções de pets, você pode procurar no site: ")
            dispatcher.utter_message(text="https://adotar.com.br/busca.aspx?cc=1484&cn=ms-campo-grande") 
        else:
            dispatcher.utter_message(text="Infelizmente não encontramos nenhum resultado para sua busca. Você pode fazer uma busca mais aprofundada nesse site:")
            dispatcher.utter_message(text="https://adotar.com.br/busca.aspx?cc=1484&cn=ms-campo-grande")
            
        return []

#================================================================== 
# ActionAnswerDisease - implementa uma função para falar  
# sobre as zoonoses
#==================================================================

# dicionario para definir a intent do usuário em relação ao faq de doenças
QUESTION = {
     "prevenção": "prevent",
     "tratamentos":"treatments",
     "sintomas":"symptoms" ,
     "sintoma":"symptoms",
     "prevenir":"prevent",
     "tratamento":"treatments",
     "tratar":"treatments"
 }
class ActionAnswerDisease(Action):

    def name(self) -> Text:
        return "action_answer_disease"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # pega os slots que irão o faq das doenças
        disease_slot = tracker.get_slot("disease")
        question_slot = tracker.get_slot("question")

        # logica para fazer a utterance das doenças
        if question_slot and QUESTION[question_slot]:
            utter_response_answer = 'utter_askaction/ask_{question}_{disease}'.format(disease=disease_slot,question=QUESTION[question_slot])
        else:
            utter_response_answer = 'utter_askaction/ask_initial_info_{disease}'.format(disease=disease_slot)
        
        dispatcher.utter_message(response=utter_response_answer)

        return [SlotSet("disease",None),SlotSet("question",None)]


#================================================================== 
# ActionsReset- implementa os resets 
# nos slots do volunteer_form
#==================================================================
class ActionResetVolunteerSlots(Action):

     def name(self) -> Text:
        return "action_reset_volunteer_slots"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("email_slot", None), SlotSet("contact_number_slot", None), SlotSet("how_to_help_slot", None)]

#================================================================== 
# ActionsReset- implementa os resets 
# nos sots do pet_form
#==================================================================
class ActionResetPetSlots(Action):

     def name(self) -> Text:
        return "action_reset_pet_slots"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("animal_type_slot", None), SlotSet("size_slot", None), SlotSet("age_slot", None), SlotSet("gender_slot", None)]

#================================================================== 
# ActionsReset- implementa os resets 
# nos slots do donate_form
#==================================================================
class ActionResetDonateSlot(Action):

     def name(self) -> Text:
        return "action_reset_donate_slot"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("what_to_donate_slot", None)]

#================================================================== 
# ActionsReset- implementa os resets 
# no slot do nome
#==================================================================

class ActionResetNameSlot(Action):

     def name(self) -> Text:
        return "action_reset_name_slot"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("name_slot", None)]
