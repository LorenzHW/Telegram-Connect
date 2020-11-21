from datetime import tzinfo
from skill.i18n.language_model_abc import LanguageModelABC


class LanguageModelDE(LanguageModelABC):
    def __init__(self, timezone: tzinfo):
        self.timezone = timezone
        self.SKILL_NAME = 'Telegram Connect'
        self.SKILL_NAME_SPOKEN_EN = "<lang xml:lang='en-US'>Telegram Connect</lang>".format(self.SKILL_NAME)

        self.set_language_model()

    def set_language_model(self):
        ##############################
        # GeneralStuff
        ##############################
        self.ACKS = ["Okay", "Alles klar", "Okey Dokey"]
        self.ACCEPTANCE_ACKS = ["Okay", "Ok"]
        self.DONE_ACKS = ["Okay"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Gibt es noch etwas?", "Kann ich dir noch helfen?",
                              "Brauchst du noch etwas?"]
        self.GOODBYES = ["Tschüss", "Ciao", "Bis dann", "Bis später"]
        self.DONT_UNDERSTAND = ["Entschuldigung"]

        self.GOOD_EVENING = "Guten Abend!"
        self.GOOD_MORNING = "Guten morgen!"
        self.GOOD_AFTERNOON = "Guten Nachmittag!"
        self.GOOD_BYE_EVENING = "Schönen Abend noch!"
        self.GOOD_BYE_MORNING = "Schönen Tag noch!"

        self.FALLBACK = self.get_random_dont_understand() + ", was hast du gesagt?"
        self.EXCEPTION = "Ein unerwarteter Fehler ist aufgetreten. Wenn du Zeit hast, lass uns auf <lang xml:lang='en-US'>GitHub</lang> wissen was passiert ist." \
                         " Bis später"

        ##############################
        # LaunchRequestHandler
        ##############################
        self.WELCOME_BACK = 'Willkommen zurück!'
        self.NO_NEW_TELEGRAMS = "Du hast kein neues Telegramm."
        self.NEW_TELEGRAMS = 'Du hast neue Telegramme. Möchtest du sie hören?'
        self.NEW_SETUP = 'Willkommen bei {}. {} verbindet Alexa mit dem Telegram Messenger. Bist du bereit, dass ' \
                         'Setup zu starten?'.format(self.SKILL_NAME_SPOKEN_EN, self.SKILL_NAME_SPOKEN_EN)

        ##############################
        # HelpIntent
        ##############################
        self.HELP = "{} verbindet Alexa mit dem Telegram Messenger. Um " \
                    "das Setup zu starten sage: 'Starte das Setup'. Um zu schauen ob du neue Telegramme hast sage: 'checke " \
                    "meine Telegramme'. Wenn du mehr über den Skill erfahren möchtest, sage: 'Lerne mehr über den Skill'. " \
                    "Also, was möchtest du machen?".format(self.SKILL_NAME_SPOKEN_EN)
        self.RATE_SKILL = "Wenn dir {} gefällt, schreibe eine Bewertung auf Amazon. Wir schätzen jegliche Art von " \
                          "Feedback und versuchen den Skill durchgehend zu verbessern. Danke!" \
            .format(self.SKILL_NAME_SPOKEN_EN)

        ##############################
        # SetupIntent
        ##############################
        self.NO_PERMISSION = 'Du gewährst {} keinen Zugriff auf deine Telefonnummer. ' \
                             'Um deinen Telegram Messenger mit Alexa zu koppeln, benötigen wir den Zugriff. ' \
                             'Öffne die Alexa App und gestatte den entsprechenden Zugriff. Bis später.' \
            .format(self.SKILL_NAME_SPOKEN_EN)

        self.CODE_SENT = 'Nimm dein Telefon und öffne Telegram. ' + self.BREAK_2000 + 'Du hast soeben einen Code erhalten. Wie lautet der Code?'
        self.SUCCESS_SETUP = 'Du hast Alexa erfolgreich mit Telegram verknüpft. Um zu checken ob du neue Nachrichten hast, starte den Skill neu. Bis später.'
        self.PHONE_CODE_INVALID = '{} ist der falsche Code. Bitte sage den Code erneut.'
        self.PHONE_CODE_INVALID_2 = '{} ist wieder der falsche Code. Bitte versuche es später noch ein mal. Tschüss.'
        self.PHONE_CODE_EXPIRED = 'Der Code ist bereits abgelaufen. Tschüss.'
        self.PHONE_NUM_UNOCCUPIED = 'Diese Telefonnummer kennt Telegram nicht. Bitte erstelle zuerst einen Telegram Account und dann kannst du diesen Skill verwenden. Bis dann.'
        self.TWO_STEP_ON = "Du hast die Zwei-Schritt Verifizierung in Telegram aktiviert. Alexa kann mit Telegram nicht gekoppelt werden solange diese an ist. Gehe zuerst in deine Telegram App und deaktiviere Zwei-Schritt Verifizierung. Dann kannst du es noch einmal probieren. Nachdem du Alexa erfolgreich mit Telegram verknüpft hast, kannst du Zwei-Schritt Verifiezierung wieder anschalten. Bis später."
        self.ALREADY_AUTHORIZED = 'Du hast Alexa bereits erfolgreich mit Telegram veknüpft. Bis später.'
        self.EXCEPTION_RETRIEVING_PHONE_NUM = 'Es gab ein Problem deine Telefonnummer von deinem Amazon Account zu ermitteln. Vergewissere, dass Telegram Connect die nötigen Berechtigungen hat um auf dein Amazon Profil zugreifen zu können und das du eine Telefonnummer hintelegt hast. Bis später.'

        ##############################
        # MessageIntent
        ##############################
        self.NEW_TELEGRAMS_FROM = 'Du hast neue Telegramme erhalten von: {}. '
        self.AND = 'und'
        self.NO_MORE_TELEGRAMS = 'Es gibt keine weiteren Telegramme. Bis später.'
        self.NEXT_TELEGRAMS = 'Möchtest du die Telegramme vom nächsten Kontakt hören?'
        self.PERSONAL_DIALOG_INTRO = '{} schrieb: '
        self.GROUP_DIALOG_INTRO = 'In {}'
        self.MEDIA_FILE_RECEIVED = '{} hat eine Datei geschickt.'
        self.NOT_AUTHORIZED = "Du hast Alexa nicht mit Telegram veknüpft. Bis später."

        ##############################
        # YesIntent
        ##############################
        self.SUGGEST_WHAT_TO_DO = " Folgendes kannst du sagen: 'Checke meine Telegramm' or: 'Lerne mehr über den Skill'. Also, was möchtest du machen?"

        ##############################
        # LearnMoreIntent
        ##############################
        self.LEARN_MORE = "{} koppelt Alexa mit Telegram. Der Code für diesen Skill ist open-source und jeder " \
                          "ist willkommen mitzuarbeiten. Wir suchen Leute die den Skill in verschiedene Sprachen übersetzen " \
                          "wie zum Beispiel italienisch oder spanisch. Wenn du Probleme mit diesem Skill hast " \
                          "oder ein Feature vermisst, melde dich bei uns auf <lang xml:lang='en-US'>GitHub</lang>. Bis dann." \
            .format(self.SKILL_NAME_SPOKEN_EN)
