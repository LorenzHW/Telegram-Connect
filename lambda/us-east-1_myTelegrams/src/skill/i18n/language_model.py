from src.skill.i18n.generic_language_model import GenericLanguageModel


class LanguageModel(GenericLanguageModel):
    def __init__(self, locale):
        super().__init__(locale)
        self.FIRST_NAME = None
        self.FIRST_NAME_REPROMPT = None
        self.MESSAGE = None
        self.MESSAGE_REPROMPT = None
        self.NO_CONTACT = None
        self.NO_CONTACT_2 = None
        self.NO_CONTACT_REPROMPT = None
        self.NO_CONTACT_REPROMPT_2 = None
        self.MAX_NO_CONTACT = None

        self.REPLY = None
        self.NEW_TELEGRAMS = None
        self.REPLY_SEND_OR_STOP = None
        self.NO_TELEGRAMS = None
        self.AND = None
        self.GROUP_INTRO = None
        self.GROUP_MESSAGE_INTRO = None
        self.PERSONAL_CHAT_INTRO = None
        self.MEDIA_FILE = None
        self.BREAK_BETWEEN_NAMES = None
        self.BREAK_BETWEEN_TELEGRAMS = None

        self.NOT_AUTHORIZED = None
        self.USER_HAS_TELEGRAMS = None

        self.TELEGRAM_SENT = None
        self.MESSAGE_2 = None

        self.HELP_USER = None
        self.YES = None
        self.NO  = None

        self.NO_PHONE = None
        self.WHAT_IS_CODE = None
        self.WHAT_IS_CODE_REPROMPT = None
        self.WRONG_CODE = None
        self.AUTHORIZED = None

        self.SPEED_DIAL = None
        self.SPEED_DIAL_REPROMPT = None
        self.NO_SPEED_DIAL_CONTACT = None
        self.MULTIPLE_TELEGRAM_CONTACTS_FOR_SPEED_DIAL = None

        self.SETTINGS_OPENED = None
        self.NON_VERBOSE_CHOICE = None
        self.ENABLE = None
        self.DISABLE = None
        self.LEAVING_SETTINGS_MODE = None

        self.INVALID_PHONE = None
        self.CODE_EXPIRED = None
        self.CODE_INVALID = None
        self.TWO_STEPS_VERIFICATION_ERROR = None
        self.FLOODWAIT_ERROR = None
        self.CHAT_ADMIN_REQUIRED_ERROR = None
        self.NOT_AUTHORIZED_DETOUR = None
        self.BYE_FOR_NOW = None

    def set_german_language_model(self):
                ### SendIntent ###
        self.FIRST_NAME = self.get_random_ack() + ", wie lautet der Vorname oder die Kurzwahl?"
        self.FIRST_NAME_REPROMPT = self.get_random_dont_understand() + ", wie war der Name oder die Zahl?"
        self.MESSAGE = self.get_random_acceptance_ack() + ", wie lautet das Telegram für {}?"
        self.MESSAGE_REPROMPT = self.get_random_dont_understand() + ", wie lautet das Telegram für {}?"
        self.NO_CONTACT = self.get_random_thinking() + ", Ich konnte keinen Kontakt mit diesem Namen finden. Es gibt: <break time='100ms'/> 1 <break time='150ms'/> {}, <break time='100ms'/> 2 <break time='150ms'/> {}, und <break time='100ms'/> 3 <break time='150ms'/> {}. Zu wem soll ich das Telegram schicken?"
        self.NO_CONTACT_2 = self.get_random_thinking() + ", Ich konnte keinen Kontakt mit diesem Namen finden. Es gibt: <break time='100ms'/> 1 <break time='150ms'/> {}, und <break time='100ms'/> 2 <break time='150ms'/> {}. Zu wem soll ich das Telegram schicken?"
        self.NO_CONTACT_REPROMPT = self.get_random_dont_understand() + ", Das habe ich jetzt nicht verstanden. Es gibt: <break time='100ms'/> 1 <break time='150ms'/> {}, <break time='100ms'/> 2 <break time='150ms'/> {}, und <break time='100ms'/> 3 <break time='150ms'/> {}. Zu wem soll ich das Telegram schicken?"
        self.NO_CONTACT_REPROMPT_2 = self.get_random_dont_understand() + ", Das habe ich jetzt nicht verstanden. Es gibt: <break time='100ms'/> 1 <break time='150ms'/> {}, und <break time='100ms'/> 2 <break time='150ms'/> {}. Zu wem soll ich das Telegram schicken?"
        self.MAX_NO_CONTACT = "Sorry. Ich habe immer noch Probleme dich zu verstehen. Bitte sage eine der Ganzzahlen: <break time='100ms'/> 1 <break time='150ms'/> <break time='100ms'/> 2 <break time='150ms'/> oder <break time='100ms'/> 3 <break time='150ms'/>. Als alternative kannst du die Kurzwahl Funktion probieren. Schau in der Skill beschreibung nach wie das funktioniert. " + self.get_random_goodbye()

        ### MessageIntent ###
        self.REPLY_OR_NEXT_TELEGRAM = "<break time='250ms'/> Möchtest du antworten oder das nächste Telegram hören?"
        self.NEW_TELEGRAMS = "Du hast neue Telegramme von: "
        self.REPLY_SEND_OR_STOP = " Möchtest du antworten, ein Telegram an eine andere Person verschicken oder stoppen?"
        self.NO_TELEGRAMS = "Du hast keine neue Telegramme. " + self.get_random_anyting_else_without_ack()
        self.AND = ", und "
        self.GROUP_INTRO = "In {}: <break time='200ms'/>"
        self.GROUP_MESSAGE_INTRO = "{} schrieb: <break time='100ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} schrieb: <break time='200ms'/>"
        self.MEDIA_FILE = "Medien Datei"
        self.BREAK_BETWEEN_NAMES = self.BREAK_200
        self.BREAK_BETWEEN_TELEGRAMS = self.BREAK_150

        ### LaunchIntent ###
        self.NOT_AUTHORIZED = "Willkommen bei {}. {} verbindet den Telegram Messenger mit Alexa. Nun, möchtest du mehr Informationen hören oder die Autorisierung starten?" \
            .format(self.skill_name, self.skill_name)
        self.USER_HAS_TELEGRAMS = "Willkommen zurück bei {}. Du hast neue Telegramme. Möchtest du sie hören?" \
            .format(self.skill_name)
        self.WELCOME = "Willkommen zurück bei {}. Ich kann dir helfen ein Telegram zu verschicken oder zu checken ob es neue gibt. Also, was brauchst du?" \
            .format(self.skill_name)

        ### ReplyIntent ###
        self.TELEGRAM_SENT = self.get_random_done_ack() + ", ein Telegram wurde an {} verschickt. <break time='200ms'/>"
        self.MESSAGE_2 = "Wie lautet das Telegram?"

        ### YesIntent / NoIntent ###
        self.HELP_USER = "Ich kann dir helfen ein Telegram zu verschicken oder zu checken ob es neue gibt. Also, was brauchst du?"
        self.YES = "Ja"
        self.NO  = "Nein"

        ### AuthorizationIntent ###
        self.NO_PHONE = "Du hast noch keine Telefonnummer hinzugefügt. Besuche die Webseite die in der Skillbeschreibung steht und füge eine Telefonnummer hinzu. Bis später."
        self.WHAT_IS_CODE = "Du hast einen Code auf deinem Telefon erhalten. <break time='200ms' /> Wie lauten die Zahlen von dem Code?"
        self.WHAT_IS_CODE_REPROMPT = "Checke dein Telefon. Wie lauten die Zahlen von dem Code?"
        self.WRONG_CODE = "Der Code ist falsch. Sage den Code Zahl nach Zahl. Versuche es erneut indem du neu startest."
        self.AUTHORIZED = self.get_random_acceptance_ack() + ". Du bist autorisiert. <break time='200ms'/> Ich kann dir helfen ein Telegram zu verschicken oder zu checken ob es neue gibt. Also, was brauchst du?"

        ## SpeedDialIntent ##
        self.SPEED_DIAL = "Wie lautet die Nummer von deinem Kurzwahl Kontakt?"
        self.SPEED_DIAL_REPROMPT = self.get_random_dont_understand() + ", wie lautet die Nummer?"
        self.NO_SPEED_DIAL_CONTACT = self.get_random_thinking() + ", Ich kann keinen Kurzwahl Kontakt mit dieser Nummer finden. Bis später."
        self.MULTIPLE_TELEGRAM_CONTACTS_FOR_SPEED_DIAL = self.get_random_thinking() + ", Ich habe mehrere Kontakt mit diesen Namen gefunden. Bitte versichere, dass der Vorname von deinem Kurzwahl Kontakt genau so lautet wie er im Telegram Messenger angezeigt wird. Bis später."

        ## SettingsIntent ##
        self.SETTINGS_OPENED = 'Du bist jetzt in den Einstellungen. Möchtest du den wortarmen Modus einschalten?'
        self.NON_VERBOSE_CHOICE = 'Du hast den weniger wortreichen Modus {}.'
        self.ENABLE = 'eingeschaltet'
        self.DISABLE = 'ausgeschaltet'
        self.LEAVING_SETTINGS_MODE = 'Du verlässt jetzt die Einstellungen.'

        ## Errors ##
        self.INVALID_PHONE = "Es existiert kein Telegram Account zu dieser Telefonnummer. Erstelle einen Telegram Account zuerst, bevor du diesen Skill verwendest. Bis später."
        self.CODE_EXPIRED = "Der Code ist bereits abgelaufen. Versuche es erneut. Bis später."
        self.CODE_INVALID = "Der Code ist ungültig. Sage den Code Zahl für Zahl. Bis später."
        self.TWO_STEPS_VERIFICATION_ERROR = "Zwei Schritt Verifizierung ist nicht unterstützt. Deaktiviere Zwei Schritt Verifizierung in Telegram und versuche es erneut. Danach kannst du Zwei Schritt Verifizierung wieder aktivieren. Bis später."
        self.FLOODWAIT_ERROR = "Aufgrund von Server Wartung ist der Skill nicht verfügbar. Du kannst den Skill in {} Stunden und {} Minuten wider verwenden. Bis später."
        self.CHAT_ADMIN_REQUIRED_ERROR = "Dir fehlen die Berechtigungen um ein Telegram zu verschicken."
        self.NOT_AUTHORIZED_DETOUR = "Du bist momentan nicht authorisiert. Bitte authorisiere dich zuerst bevor du den Skill verwendest. Um mit der Autorisierung zu beginnen sage: 'Alexa, starte {}'. Bis später".format(
            self.skill_name)
        self.BYE_FOR_NOW = "Bis später."


    def set_english_language_model(self):
        ### SendIntent ###
        self.FIRST_NAME = self.get_random_ack() + ", what is the first name or speed dial number of your contact?"
        self.FIRST_NAME_REPROMPT = self.get_random_dont_understand() + ", what was the first name or the number?"
        self.MESSAGE = self.get_random_acceptance_ack() + ", what is the Telegram for {}?"
        self.MESSAGE_REPROMPT = self.get_random_dont_understand() + ", what is the Telegram for {}?"
        self.NO_CONTACT = self.get_random_thinking() + ", I can't find any contact with that name. I found: <break time='100ms'/> 1 <break time='150ms'/> {}, <break time='100ms'/> 2 <break time='150ms'/> {}, and <break time='100ms'/> 3 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.NO_CONTACT_2 = self.get_random_thinking() + ", I can't find any contact with that name. I found <break time='100ms'/> 1 <break time='150ms'/> {}, and <break time='100ms'/> 2 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.NO_CONTACT_REPROMPT = self.get_random_dont_understand() + ", I didn't catch that. I found: <break time='100ms'/> 1 <break time='150ms'/> {}, <break time='100ms'/> 2 <break time='150ms'/> {}, and <break time='100ms'/> 3 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.NO_CONTACT_REPROMPT_2 = self.get_random_dont_understand() + ", I didn't catch that. I found: <break time='100ms'/> 1 <break time='150ms'/> {}, and <break time='100ms'/> 2 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.MAX_NO_CONTACT = "Sorry. I am still having trouble understanding you. Please say: <break time='100ms'/> 1 <break time='150ms'/> <break time='100ms'/> 2 <break time='150ms'/> or <break time='100ms'/> 3 <break time='150ms'/>. Otherwise you can try out the speed dial feature. Check the skill description for more information. " + self.get_random_goodbye()

        ### MessageIntent ###
        self.REPLY_OR_NEXT_TELEGRAM = "<break time='250ms'/> Do you want to reply or listen to the next Telegram?"
        self.NEW_TELEGRAMS = "You got new Telegrams from: "
        self.REPLY_SEND_OR_STOP = " Do you want to reply, send a Telegram to someone else, or stop?"
        self.NO_TELEGRAMS = "You got no new telegrams. " + self.get_random_anyting_else_without_ack()
        self.AND = ", and "
        self.GROUP_INTRO = "In {}: <break time='200ms'/>"
        self.GROUP_MESSAGE_INTRO = "{} wrote: <break time='100ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} wrote: <break time='200ms'/>"
        self.MEDIA_FILE = "Media file"
        self.BREAK_BETWEEN_NAMES = self.BREAK_200
        self.BREAK_BETWEEN_TELEGRAMS = self.BREAK_150

        ### LaunchIntent ###
        self.NOT_AUTHORIZED = "Welcome to {}. {} let's you connect your Telegram Messenger with Alexa. Now, do you want to hear more information or start the authorization?" \
            .format(self.skill_name, self.skill_name)
        self.USER_HAS_TELEGRAMS = "Welcome to {}. You got new telegrams. Do you want to hear them?" \
            .format(self.skill_name)
        self.WELCOME = "Welcome to {}. I can help you to send a Telegram or check for new Telegrams. So, which do you need?" \
            .format(self.skill_name)

        ### ReplyIntent ###
        self.TELEGRAM_SENT = self.get_random_done_ack() + ", a Telegram was sent to {}. <break time='200ms'/>"
        self.MESSAGE_2 = "What is the Telegram?"

        ### YesIntent / NoIntent ###
        self.HELP_USER = "I can help you to send a Telegram or check for new Telegrams. So, which do you need?"
        self.YES = "Yes"
        self.NO  = "No"

        ### AuthorizationIntent ###
        self.NO_PHONE = "You have not added a telephone number. Visit the website mentioned in the skill description and add a telephone number then try again. Bye for now."
        self.WHAT_IS_CODE = "You received a code on your phone. <break time='200ms' /> What are the digits of the code?"
        self.WHAT_IS_CODE_REPROMPT = "Check your phone. What are the digits?"
        self.WRONG_CODE = "The code is wrong. Say the code digit after digit. Try requesting a new code by starting over. Bye for now."
        self.AUTHORIZED = self.get_random_acceptance_ack() + ". You are now authorized. <break time='200ms'/> I can help you send a Telegram or check for new Telegrams. So, which do you need?"

        ## SpeedDialIntent ##
        self.SPEED_DIAL = "What is the number of your speed dial contact?"
        self.SPEED_DIAL_REPROMPT = self.get_random_dont_understand() + ", what number?"
        self.NO_SPEED_DIAL_CONTACT = self.get_random_thinking() + ", I can't find any speed dial contact with that number. Bye for now."
        self.MULTIPLE_TELEGRAM_CONTACTS_FOR_SPEED_DIAL = self.get_random_thinking() + ", I found multiple contacts with that first name. Please check that the first name of your Telegram contact matches exactly the first name of your speed dial contact. Bye for now."

        ## SettingsIntent ##
        self.SETTINGS_OPENED = 'You are now in the Settings mode. Do you want to enable non-verbose mode?'
        self.NON_VERBOSE_CHOICE = 'You {} non-verbose mode.'
        self.ENABLE = 'enable'
        self.DISABLE = 'disable'
        self.LEAVING_SETTINGS_MODE = 'You are now leaving settings mode.'

        ## Errors ##
        self.INVALID_PHONE = "There is no Telegram account associated with that phone number. Create a Telegram Account first, before you can use that skill. Bye for now."
        self.CODE_EXPIRED = "The code already expired. Try it again. Bye for now."
        self.CODE_INVALID = "The code is invalid. Bye for now."
        self.TWO_STEPS_VERIFICATION_ERROR = "Two step verification is not supported. Please deactivate two step verficication in Telegram to use this skill. You can activate two steps verification again afterwards. Bye for now."
        self.FLOODWAIT_ERROR = "The skill is unavailable due to server maintenance. You can use this skill in {} hours and {} minutes. Bye for now."
        self.CHAT_ADMIN_REQUIRED_ERROR = "You don't have the privilege to send a Telegram."
        self.NOT_AUTHORIZED_DETOUR = "You are currently not authorized. Please authorize first if you want to use all features of this skill. To start the authorization process say: 'Alexa, start {}'. Bye for now".format(
            self.skill_name)
        self.BYE_FOR_NOW = "Bye for now."
