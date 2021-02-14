from datetime import tzinfo
from skill.i18n.language_model_abc import LanguageModelABC


class LanguageModelIT(LanguageModelABC):
    def __init__(self, timezone: tzinfo):
        self.timezone = timezone
        self.SKILL_NAME = 'Telegram Connect'
        self.SKILL_NAME_SPOKEN_IT = "<lang xml:lang='it-IT'>Telegram Connect</lang>".format(self.SKILL_NAME)

        self.set_language_model()

    def set_language_model(self):
        ##############################
        # GeneralStuff
        ##############################
        self.ACKS = ["Okay", "Va bene", "Okaaay"]
        self.ACCEPTANCE_ACKS = ["Okay", "Sicuro", "Va bene", "Ricevuto", "You got it"]
        self.DONE_ACKS = ["Okay", "Va bene", "Ricevuto", "Fatto", "You got it"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["C'è altro?", "C'è altro che posso fare per te?",
                              "Hai bisogno di altro?", "C'è altro di cui hai bisogno?"]
        self.GOODBYES = ["Ciao", "Stammi bene", "Ciao ciao", "A dopo", "Ciaaao", "Passo e chiudo", "Abbi cura di te",
                         "Arrivederci", "A più tardi", "A più tardi", "A presto", "Ci sentiamo dopo",
                         "Alla prossima", "Divertiti", "Passa una buona giornata!"]
        self.DONT_UNDERSTAND = ["Scusa", "Scusami", "Perdonami"]

        self.GOOD_EVENING = "Buonasera!"
        self.GOOD_MORNING = "Buongiorno!"
        self.GOOD_AFTERNOON = "Buon pomeriggio!"
        self.GOOD_BYE_EVENING = "Passa una buona serata!"
        self.GOOD_BYE_MORNING = "Passa una buona giornata!"

        self.FALLBACK = self.get_random_dont_understand() + ", cosa hai detto?"
        self.EXCEPTION = "Si è verificato un errore inaspettato. Se hai un po di tempo, dai il tuo feedbeck su " \
                         "GitHub. A presto."

        ##############################
        # LaunchRequestHandler
        ##############################
        self.WELCOME_BACK = 'Bentornato!'
        self.NO_NEW_TELEGRAMS = "Non hai nuovi messaggi telegram"
        self.NEW_TELEGRAMS = 'Hai nuovi messaggi telegram. Vuoi ascoltarli?'
        self.NEW_SETUP = 'Benvenuto a {}. {} integra Alexa con Telegram ' \
                         'Messenger. Sei pronto alla configurazione?'.format(self.SKILL_NAME_SPOKEN_IT,
                                                                                    self.SKILL_NAME_SPOKEN_IT)

        ##############################
        # HelpIntent
        ##############################
        self.HELP = "{} integra Alexa con Telegram Messenger. Per " \
                    "inziare la configurazione dimmi: 'Inizia la configurazione'. Per controllare se hai dei messaggi telegram dimmi: 'controlla i miei " \
                    "messaggi telegram'. Per saperne di più su questa skill, dimmi: 'voglio saperne di più'. Cosa vuoi fare ?".format(self.SKILL_NAME_SPOKEN_IT)
        self.RATE_SKILL = "Se trovi {} utile, condividi la tua opinione con gli altri utenti, scrivendo una recensione. Diamo valore " \
                          "al tuo feedback, perché ci permettere di migliorare con costanza. Grazie!" \
            .format(self.SKILL_NAME_SPOKEN_IT)

        ##############################
        # SetupIntent
        ##############################
        self.NO_PERMISSION = 'Non hai permesso a {} di accedere al tuo numero di telefono. ' \
                             'Per connettere Telegram Messenger ad Alexa, il permesso è richiesto. Apri Alexa sul tuo telefono e concedi i permessi necessari. A presto.'.format(self.SKILL_NAME_SPOKEN_IT)

        self.CODE_SENT = 'Prendi il tuo telefono ed apri Telegram. ' + self.BREAK_2000 + 'Hai appena ricevuto un codice. Puoi dettarmelo?'
        self.SUCCESS_SETUP = 'Operazione conclusa, il tuo account Telegram è collegato. Per controllare se hai ricevuto nuovi messaggi, avvia di nuovo la skill. A dopo.'
        self.PHONE_CODE_INVALID = 'Il codice {} è sbagliato. Perfavore, ripetilo.'
        self.PHONE_CODE_INVALID_2 = 'Il codice {} è ancora sbagliato. A dopo.'
        self.PHONE_CODE_EXPIRED = 'Il codice dettato è scaduto. A dopo.'
        self.PHONE_NUM_UNOCCUPIED = 'Questo numero di telefono non è collegato ad un account Telegram. Creane uno. A dopo.'
        self.TWO_STEP_ON = "Il tuo account Telegram è protetto dalla verifica a due passaggi. Alexa non può connettersi. Perfavore, disabilitala e riprova la configurazione. Quando la configurazione sarà riuscita, potrai riattivarla. A dopo."
        self.ALREADY_AUTHORIZED = 'Hai già un account di Telegram integrato con Alexa. A dopo.'
        self.EXCEPTION_RETRIEVING_PHONE_NUM = 'Non riesco ad ottenere il tuo numero di telefono dal profilo Amazon. Accertati di aver concesso a Telegram Connect il permesso di ottenere il tuo numero e che lo stesso sia valido nel tuo profilo Amazon. A dopo.'

        ##############################
        # MessageIntent
        ##############################
        self.NEW_TELEGRAMS_FROM = 'Hai ricevuto nuovi messaggi telegram da: {}. '
        self.AND = 'e'
        self.NO_MORE_TELEGRAMS = 'Non ci sono più messaggi telegram. A dopo.'
        self.NEXT_TELEGRAMS = 'Vuoi ascoltare altri messaggi telegram?'
        self.PERSONAL_DIALOG_INTRO = '{} ha scritto: '
        self.GROUP_DIALOG_INTRO = 'In {}'
        self.MEDIA_FILE_RECEIVED = '{} ha inviato un file multimediale.'
        self.NOT_AUTHORIZED = "Non hai integrato Alexa con Telegram. A dopo."

        ##############################
        # YesIntent
        ##############################
        self.SUGGEST_WHAT_TO_DO = "Puoi provare a dire: 'Controlla i miei messaggi telegram' oppure: 'voglio saperne di più'. Cosa vuoi fare?"

        ##############################
        # LearnMoreIntent
        ##############################
        self.LEARN_MORE = '{} integra Alexa con Telegram. Il codice di questa skill è open-source e le contribuzioni sono ' \
                          'ben accette. Stiamo cercando persone che traducano questa skill nella loro lingua nativa '\
                          'Se hai qualche problema oppure desideri una funzione specifica ' \
                          'contattaci su GitHub. A dopo.' \
            .format(self.SKILL_NAME_SPOKEN_IT)
