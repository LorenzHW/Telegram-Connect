from skill.i18n.language_model import LanguageModel

class NonVerboseLanguageModel(LanguageModel):
    def __init__(self, locale, non_verbose_mode):
        super().__init__(locale)

        if locale == "de-DE":
            self.set_german_language_model()
            if non_verbose_mode:
                self.set_german_non_verbose_model()
        elif locale == "it-IT":
            self.set_italian_language_model()
            if non_verbose_mode:
                self.set_italian_non_verbose_model()
        else:
            self.set_english_language_model()
            if non_verbose_mode:
                self.set_english_non_verbose_model()



    def set_german_non_verbose_model(self):
        ### SendIntent ###
        self.FIRST_NAME = "Vorname oder Kurzwahl Nummer?"
        self.MESSAGE = "Ok. {}. Telegram?"
        self.NO_CONTACT = "Es gibt: <break time='25ms'/> 1 <break time='75ms'/> {}, <break time='50ms'/> 2 <break time='75ms'/> {}, und <break time='50ms'/> 3 <break time='75ms'/> {}."
        self.NO_CONTACT_2 = "Es gibt <break time='25ms'/> 1 <break time='75ms'/> {}, und <break time='50ms'/> 2 <break time='75ms'/> {}."

        ### MessageIntent ###
        self.REPLY_OR_NEXT_TELEGRAM = "<break time='100ms'/> Antworten oder nächstes Telegram?"
        self.NEW_TELEGRAMS = "Neue Telegramme von: "
        self.REPLY_SEND_OR_STOP = "Antworten, verschicke ein neues Telegram, oder stoppe?"
        self.NO_TELEGRAMS = "Keine Telegramme. Noch was?"
        self.GROUP_INTRO = "In {}: <break time='100ms'/>"
        self.GROUP_MESSAGE_INTRO = "{} schrieb: <break time='50ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} schrieb: <break time='50ms'/>"
        self.BREAK_BETWEEN_NAMES = self.BREAK_100
        self.BREAK_BETWEEN_TELEGRAMS = self.BREAK_75

        ### LaunchIntent ###
        self.USER_HAS_TELEGRAMS = "Willkommen. Höre jetzt deine neuen Telegramme?"
        self.WELCOME = "Willkommen"

        ### ReplyIntent ###
        self.TELEGRAM_SENT = "Ein Telegram wurde an {} verschickt. <break time='100ms'/>"
        self.MESSAGE_2 = "Wie lautet das Telegram?"

        ### YesIntent ###
        self.HELP_USER = "Verschicke ein Telegram oder checke ob es neue gibt?"

        ## SpeedDialIntent ##
        self.SPEED_DIAL = "Kurzwahl Kontakt Nummer?"
        self.NO_SPEED_DIAL_CONTACT ="Kein Kurzwahl Kontakt mit dieser Nummer. Bis später"


    def set_english_non_verbose_model(self):
        ### SendIntent ###
        self.FIRST_NAME = "First name or speed dial number?"
        self.MESSAGE = "Ok. {}. Telegram?"
        self.NO_CONTACT = "I found: <break time='25ms'/> 1 <break time='75ms'/> {}, <break time='50ms'/> 2 <break time='75ms'/> {}, and <break time='50ms'/> 3 <break time='75ms'/> {}."
        self.NO_CONTACT_2 = "I found <break time='25ms'/> 1 <break time='75ms'/> {}, and <break time='50ms'/> 2 <break time='75ms'/> {}."

        ### MessageIntent ###
        self.REPLY_OR_NEXT_TELEGRAM = "<break time='100ms'/> Reply or next telegram?"
        self.NEW_TELEGRAMS = "New telegrams from: "
        self.REPLY_SEND_OR_STOP = " Reply, send a telegram, or stop?"
        self.NO_TELEGRAMS = "No new telegrams. Anything else?"
        self.GROUP_INTRO = "In {}: <break time='100ms'/>"
        self.GROUP_MESSAGE_INTRO = "{} wrote: <break time='50ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} wrote: <break time='50ms'/>"
        self.BREAK_BETWEEN_NAMES = self.BREAK_100
        self.BREAK_BETWEEN_TELEGRAMS = self.BREAK_75

        ### LaunchIntent ###
        self.USER_HAS_TELEGRAMS = "Welcome. Listen to your new Telegrams?"
        self.WELCOME = "Welcome"

        ### ReplyIntent ###
        self.TELEGRAM_SENT = "A Telegram was sent to {}. <break time='100ms'/>"
        self.MESSAGE_2 = "What is the Telegram?"

        ### YesIntent ###
        self.HELP_USER = "Sent Telegram or check Telegrams?"

        ## SpeedDialIntent ##
        self.SPEED_DIAL = "Number of speed dial contact?"
        self.NO_SPEED_DIAL_CONTACT ="No speed dial contact with that number. Bye for now."


    def set_italian_non_verbose_model(self):
        ### SendIntent ###
        self.FIRST_NAME = "Nome o numero speed dial?"
        self.MESSAGE = "Ok. {}. Telegram?"
        self.NO_CONTACT = "Ho trovato: <break time='25ms'/> 1 <break time='75ms'/> {}, <break time='50ms'/> 2 <break time='75ms'/> {}, e <break time='50ms'/> 3 <break time='75ms'/> {}."
        self.NO_CONTACT_2 = "Ho trovato <break time='25ms'/> 1 <break time='75ms'/> {}, e <break time='50ms'/> 2 <break time='75ms'/> {}."

        ### MessageIntent ###
        self.REPLY_OR_NEXT_TELEGRAM = "<break time='100ms'/> Rispondi o prossimo telegram?"
        self.NEW_TELEGRAMS = "Nuovo telegram da: "
        self.REPLY_SEND_OR_STOP = " Rispond, invia un telegram, o esci?"
        self.NO_TELEGRAMS = "Nessun nuovo telegram. Altro?"
        self.GROUP_INTRO = "In {}: <break time='100ms'/>"
        self.GROUP_MESSAGE_INTRO = "{} ha scritto: <break time='50ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} ha scritto: <break time='50ms'/>"
        self.BREAK_BETWEEN_NAMES = self.BREAK_100
        self.BREAK_BETWEEN_TELEGRAMS = self.BREAK_75

        ### LaunchIntent ###
        self.USER_HAS_TELEGRAMS = "Benvenuto. Vuoi ascoltare i nuovi Telegram?"
        self.WELCOME = "Benvenuto"

        ### ReplyIntent ###
        self.TELEGRAM_SENT = "Un Telegram è stato inviato a {}. <break time='100ms'/>"
        self.MESSAGE_2 = "Qual è il Telegram?"

        ### YesIntent ###
        self.HELP_USER = "Invia Telegram o controlla nuovi Telegram?"

        ## SpeedDialIntent ##
        self.SPEED_DIAL = "Number speed dial?"
        self.NO_SPEED_DIAL_CONTACT ="Non è stato trovato nessun speed dial con quel numero. A presto."
