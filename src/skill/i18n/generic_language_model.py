import random


class GenericLanguageModel(object):
    def __init__(self, locale):
        self.skill_name = "Daily Telegrams"

        self.ERROR = None
        self.BACKEND_EXCEPTION = None
        self.SERVER_ERROR = None
        self.ACCOUNT_LINKING_REQUIRED_TITLE = None
        self.ACCOUNT_LINKING_REQUIRED = None
        self.WRONG_INTENT_TITLE = None
        self.WRONG_INTENT = None
        self.ACKS = None
        self.ACCEPTANCE_ACKS = None
        self.WELCOME_TITLE = None
        self.WELCOME = None
        self.FALLBACK_TITLE = None
        self.FALLBACK = None
        self.HELP_TITLE = None
        self.HELP = None
        self.GOODBYES = None

        if locale == "de-DE":
            self.set_generic_phrases_german()
        else:
            self.set_generic_phrases_english()

    def set_generic_phrases_german(self):
        self.ERROR = "Fehler"
        self.BACKEND_EXCEPTION = 'Das ist ein Fehler, der nicht passieren dürfte. Tut mir leid.'
        self.SERVER_ERROR = "Aufgrund von Server Updates ist dieser Skill momentan nicht " \
                            "verfügbar. Bitte versuche es später erneut "
        self.ACCOUNT_LINKING_REQUIRED_TITLE = 'Erstelle einen Account'
        self.ACCOUNT_LINKING_REQUIRED = 'Du benötigst einen {} Account um diesen Skill ' \
                                        'nutzen zu können. Bitte verwende die Alexa app um deinen ' \
                                        'Amazon Account mit dem {} Account' \
                                        ' zu verknüpfen.'.format(self.skill_name, self.skill_name)

        self.WRONG_INTENT_TITLE = "Sorry."
        self.WRONG_INTENT = "Sorry das habe ich jetzt nicht nachvollziehen können. Ich kann dir " \
                            "hier nicht weiter helfen. "

        self.ACKS = ["Okay", "In Ordnung", "Alles klar"]
        self.ACCEPTANCE_ACKS = ["Okay", "In Ordnung", "Alles klar"]
        ##############################
        # Required intents
        ##############################
        self.WELCOME_TITLE = "Willkommen"
        self.WELCOME = "Willkommen"

        self.FALLBACK_TITLE = "Sorry?"
        self.FALLBACK = "Sorry, was hast du gesagt?"

        self.HELP_TITLE = "Hilfe"
        self.HELP = "Help Intent"

        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]

    def set_generic_phrases_english(self):
        self.ERROR = "Error"
        self.BACKEND_EXCEPTION = 'This is an error that should not happen. I am sorry.'
        self.SERVER_ERROR = "Due to updates the service is currently not available." \
                            " Please try again later."
        self.ACCOUNT_LINKING_REQUIRED_TITLE = 'Create an account.'
        self.ACCOUNT_LINKING_REQUIRED = 'You must have a {} account to use this skill.' \
                                        ' Please use the Alexa app to link your Amazon account' \
                                        ' with your {} Account.'.format(self.skill_name,
                                                                        self.skill_name)

        self.WRONG_INTENT_TITLE = "Sorry."
        self.WRONG_INTENT = "I didn't quite catch that. I can't help you here."

        self.ACKS = ["Okay", "Alright"]
        self.ACCEPTANCE_ACKS = ["Okay", "Sure", "Alright", "Got it", "Done", "You got it."]
        ##############################
        # Required intents
        ##############################
        self.WELCOME_TITLE = "Welcome"
        self.WELCOME = "Welcome"

        self.FALLBACK_TITLE = "Sorry?"
        self.FALLBACK = "Sorry, what did you say?"

        self.HELP_TITLE = "Help"
        self.HELP = "Help Intent"

        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]

    def get_random_ack(self):
        return random.choice(self.ACKS)

    def get_random_acceptance_ack(self):
        return random.choice(self.ACCEPTANCE_ACKS)

    def get_random_goodbye(self):
        return random.choice(self.GOODBYES)
