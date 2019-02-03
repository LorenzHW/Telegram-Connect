import random


class GenericLanguageModel(object):
    def __init__(self, locale):
        self.skill_name = "My Telegrams"

        self.BACKEND_EXCEPTION = None
        self.FRONTEND_ERROR = None
        self.SERVER_ERROR = None
        self.ACCOUNT_LINKING_REQUIRED = None
        self.WRONG_INTENT = None
        self.ACKS = None
        self.ACCEPTANCE_ACKS = None
        self.DONE_ACKS = None
        self.THINKING = None
        self.DONT_UNDERSTAND = None
        self.WELCOME = None
        self.FALLBACK = None
        self.FALLBACK_INTENT = None
        self.FALLBACK_INTENT_REPROMPT = None
        self.HELP = None
        self.GOODBYES = None
        self.ANYTHING_ELSE = None

        self.BREAK_50 = "<break time='50ms'/>"
        self.BREAK_75 = "<break time='75ms'/>"
        self.BREAK_100 = "<break time='100ms'/>"
        self.BREAK_150 = "<break time='150ms'/>"
        self.BREAK_200 = "<break time='200ms'/>"

        if locale == "de-DE":
            self.set_generic_phrases_german()
        elif locale == "it-IT":
            self.set_generic_phrases_italian()
        else:
            self.set_generic_phrases_english()

    def set_generic_phrases_german(self):
        self.ACKS = ["Okay", "In Ordnung", "Alles klar", "Okey Dokey"]
        self.ACCEPTANCE_ACKS = ["Okay", "In Ordnung", "Alles klar"]
        self.DONE_ACKS = ["Okay", "In Ordnung", "Alles klar", "Geschafft"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Gibt es sonst noch was?",
                              "Gibt es noch etwas wobei ich dir helfen kann?",
                              "Brauchst du noch etwas?", "Noch etwas?"]
        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]
        self.DONT_UNDERSTAND = ["Sorry", "Entschuldigung", "Pardon"]

        self.BACKEND_EXCEPTION = "Das ist ein Fehler, der nicht passieren dürfte. Tut mir leid."
        self.FRONTEND_ERROR = self.get_random_thinking() + ", es ist ein Fehler aufgetreten. Versuche es später noch einmal. " + self.get_random_goodbye()
        self.SERVER_ERROR = "Aufgrund von Server Updates ist dieser Skill momentan nicht " \
                            "verfügbar. Versuche es später erneut "
        self.ACCOUNT_LINKING_REQUIRED = "Willkommen bei {}. {} verbindet Alexa mit dem Telegram Messenger. " \
                                        "Du benötigst einen {} Account um diesen Skill nutzen zu können. " \
                                        "Gehe in die Alexa App um deinen Amazon Account mit dem {} Account zu verknüpfen. " \
                                        "Besuche die Webseite die in der Skillbeschreibung steht. " \
                                        " Bis später.".format(self.skill_name, self.skill_name, self.skill_name, self.skill_name)

        self.WRONG_INTENT = "Sorry das habe ich jetzt nicht nachvollziehen können. Ich kann dir " \
                            "hier nicht weiter helfen. "

        ##############################
        # Required intents
        ##############################
        self.WELCOME = "Willkommen"
        self.FALLBACK = self.get_random_dont_understand() + ", was hast du gesagt?"
        self.FALLBACK_INTENT = "{} kann dir dabei nicht helfen. Du kannst entweder ein Telegram " \
                               "verschicken oder checken ob es neue gibt. Also, was brauchst " \
                               "du?".format(self.skill_name)
        self.FALLBACK_INTENT_REPROMPT = self.get_random_thinking() + ", ich habe das nicht " \
                                                                     "verstanden. Sage entweder: " \
                                                                     "'Versende ein Telegram' " \
                                                                     "oder 'Checke meine " \
                                                                     "Telegramme' "
        self.HELP = "Du kannst ein Telegram zu einer Person oder Gruppe schicken und ungelesene Telegramme abhören." + self.BREAK_50 + \
                    " In den Einstellungen kannst du einen wortarmen Modus aktivieren um den Skill schneller zu verwenden." + self.BREAK_50 + \
                    " Du hast folgende Befehle zur Auswahl: 'Öffne Einstellungen', 'Verschicke ein Telegram', oder 'Checke meine Telegramme'. " + self.BREAK_50 + \
                    " Falls ich beim Versenden eines Telegrams, Probleme habe den Namen zu verstehen, kannst du Gebrauch von der Kurzwahl Funktion machen. Schaue dir dafür die Skillbeschreibung an." + self.BREAK_50 + \
                    " Wenn du neue Telegramme hast und den Skill startest werde ich dich fragen ob du sie hören möchtest." + self.BREAK_50 + \
                    " Bevor du den Skill nutzen kannst musst du dich autorisieren. Falls du das noch nicht gemacht hast, sage jetzt: 'Autorisiere mich'"
                    
                    

    def set_generic_phrases_english(self):
        self.ACKS = ["Okay", "Alright", "Okey Dokey"]
        self.ACCEPTANCE_ACKS = ["Okay", "Sure", "Alright", "Got it", "You got it"]
        self.DONE_ACKS = ["Okay", "Alright", "Got it", "Done", "You got it"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Anything else?", "Is there something else I can help you with?",
                              "Do you need anything else?", "Is there something else you need?"]
        self.DONT_UNDERSTAND = ["Sorry", "Excuse me", "Pardon"]
        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]

        self.BACKEND_EXCEPTION = "This is an error that shouldn't happen. I am sorry."
        self.FRONTEND_ERROR = self.get_random_thinking() + ", an unexpected error happened. Try again later. " + self.get_random_goodbye()
        self.SERVER_ERROR = "Due to updates the service is currently not available." \
                            " Try again later."
        self.ACCOUNT_LINKING_REQUIRED = "Welcome to {}. {} let's you connect Alexa with your Telegram Messenger. " \
                                        "You must have a {} account to use this skill." \
                                        " Go to the Alexa app to link " \
                                        "your Amazon account with your {} Account. Visit the website" \
                                        " mentioned in the skill description. " \
                                        "Bye for now.".format(self.skill_name, self.skill_name,
                                                              self.skill_name, self.skill_name)

        self.WRONG_INTENT = "I didn't quite catch that. I can't help you here."

        ##############################
        # Required intents
        ##############################
        self.WELCOME = "Welcome"
        self.FALLBACK = self.get_random_dont_understand() + ", what did you say?"
        self.FALLBACK_INTENT = "{} can't help you here. You can either send a Telegram or check " \
                               "for new ones. So, which do you need?".format(self.skill_name)
        self.FALLBACK_INTENT_REPROMPT = self.get_random_thinking() + ", I am still having trouble " \
                                                                     "understanding you. You can " \
                                                                     "either say: 'Send a " \
                                                                     "telegram' or 'Check my " \
                                                                     "Telegrams' "
        self.HELP = "You can send Telegrams to a person or to a group and also check if you have new telegrams." + self.BREAK_50 + \
                    " In settings mode you can activate a non-verbose mode to use the skill faster."  + self.BREAK_50 + \
                    " You can use following commands: 'Open settings', 'Send a telegram', or 'Check my telegrams'. " + self.BREAK_50 + \
                    " If I have trouble understanding you while sending a Telegram you can make use of the speed dial feature. Check the skill description for more information." + self.BREAK_50 +\
                    " If you have new Telegrams and you start the skill, I will ask you if you want to hear them." + self.BREAK_50 + \
                    " Before you can use this skill you need to authorize. If you have not done that yet say: 'Start authorisation'" 



    def set_generic_phrases_italian(self):
        self.ACKS = ["Okay", "Va bene", "D'accordo", "Okey Dokey"]
        self.ACCEPTANCE_ACKS = ["Okay", "Certamente", "Va bene", "D'accordo", "Come desideri"]
        self.DONE_ACKS = ["Okay", "Va bene", "D'accordo", "Fatto", "Come desideri"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Serve altro?", "C'è qualche altra cosa in cui posso aiutarti?",
                              "Hai bisogno di altro?", "Posso aiutarti in altro?"]
        self.DONT_UNDERSTAND = ["Sorry", "Scusa", "Pardon"]
        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]

        self.BACKEND_EXCEPTION = "Si è verificato un imprevisto. Mi dispiace."
        self.FRONTEND_ERROR = self.get_random_thinking() + ", si è verificato un errore inatteso. Riprova più tardi. " + self.get_random_goodbye()
        self.SERVER_ERROR = "A causa di un aggiornamento, il servizio non è disponibile." \
                            " Riprova più tardi."
        self.ACCOUNT_LINKING_REQUIRED = "Benvenuto in {}. {} ti permettere di connettere Alexa con il tuo Telegram Messenger. " \
                                        "È necessario un account {} per poter utilizzare questa skill. " \
                                        "Apri la app di Alexa per collegare " \
                                        "il tuo account Amazon con il tuo account {}. Visita il sito" \
                                        " nella descrizione della skill. " \
                                        "A presto.".format(self.skill_name, self.skill_name,
                                                              self.skill_name, self.skill_name)

        self.WRONG_INTENT = "Credo di non aver capito. Non sono in grado di aiutarti."

        ##############################
        # Required intents
        ##############################
        self.WELCOME = "Benvenuto"
        self.FALLBACK = self.get_random_dont_understand() + ", puoi ripetere?"
        self.FALLBACK_INTENT = "{} non è in grado di aiutarti. Puoi inviare un messaggio Telegram oppure controllare " \
                               "nuovi messaggi. Di cosa hai bisogno?".format(self.skill_name)
        self.FALLBACK_INTENT_REPROMPT = self.get_random_thinking() + ", continuo a non capirti. " \
                                                                     "Puoi dire: 'Invia un telegram' " \
                                                                     "or 'Controlla i miei messaggi' "
        self.HELP = "Puoi inviare messaggi ad una persona o ad un gruppo e controllare se ci sono nuovi messaggi." + self.BREAK_50 + \
                    " In impostazioni puoi attivare la modalità sintetica per usare la skill più velocemente."  + self.BREAK_50 + \
                    " Puoi usare i seguenti comandi: 'Apri impostazioni', 'Invia un telegram' o 'Controlla i miei messaggi'. " + self.BREAK_50 + \
                    " Se faccio fatica a capire i tuoi telegram, prova ad usare lo speed dial. Consulta la descrizione della skill per ulteriori informazioni." + self.BREAK_50 +\
                    " Se quando avvii la skill hai nuovi telegram non letti, ti chiederò proporrò di ascoltarli." + self.BREAK_50 + \
                    " Prima di poter utilizzare questa skill c’è bisogno di autorizzarla. Se ancora non l’hai fatto, pronuncia: ‘Avvia autorizzazione'"

    def get_random_ack(self):
        return random.choice(self.ACKS)

    def get_random_acceptance_ack(self):
        return random.choice(self.ACCEPTANCE_ACKS)

    def get_random_done_ack(self):
        return random.choice(self.DONE_ACKS)

    def get_random_goodbye(self):
        return random.choice(self.GOODBYES)

    def get_random_thinking(self):
        return random.choice(self.THINKING)

    def get_random_anyting_else(self):
        random_anyting_else = random.choice(self.ANYTHING_ELSE)
        return self.get_random_done_ack() + ". " + random_anyting_else

    def get_random_anyting_else_without_ack(self):
        return random.choice(self.ANYTHING_ELSE)

    def get_random_dont_understand(self):
        return random.choice(self.DONT_UNDERSTAND)
