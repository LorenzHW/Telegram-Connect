import random


class GenericLanguageModel(object):
    def __init__(self, locale):
        self.skill_name = "Daily Telegrams"

        self.ERROR = None
        self.BACKEND_EXCEPTION = None
        self.SERVER_ERROR = None
        self.ACCOUNT_LINKING_REQUIRED = None
        self.WRONG_INTENT = None
        self.ACKS = None
        self.ACCEPTANCE_ACKS = None
        self.DONE_ACKS = None
        self.THINKING = None
        self.WELCOME = None
        self.FALLBACK = None
        self.HELP = None
        self.GOODBYES = None

        if locale == "de-DE":
            self.set_generic_phrases_german()
        else:
            self.set_generic_phrases_english()

    def set_generic_phrases_german(self):
        self.ERROR = "Fehler"
        self.BACKEND_EXCEPTION = "Das ist ein Fehler, der nicht passieren dürfte. Tut mir leid."
        self.SERVER_ERROR = "Aufgrund von Server Updates ist dieser Skill momentan nicht " \
                            "verfügbar. Versuche es später erneut "
        self.ACCOUNT_LINKING_REQUIRED = "Du benötigst einen {} Account um diesen Skill " \
                                        "nutzen zu können. Bevor du diesen Skill verwenden kannst, benutze die Alexa app um deinen " \
                                        "Amazon Account mit dem {} Account" \
                                        " zu verknüpfen.".format(self.skill_name, self.skill_name)

        self.WRONG_INTENT = "Sorry das habe ich jetzt nicht nachvollziehen können. Ich kann dir " \
                            "hier nicht weiter helfen. "

        self.ACKS = ["Okay", "In Ordnung", "Alles klar"]
        self.ACCEPTANCE_ACKS = ["Okay", "In Ordnung", "Alles klar"]
        self.DONE_ACKS = ["Okay", "In Ordnung", "Alles klar", "Geschafft"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Gibt es sonst noch was?", "Ist das alles?",
                              "Brauchst du noch etwas?", "Noch etwas?"]

        ##############################
        # Required intents
        ##############################
        self.WELCOME = "Willkommen"
        self.FALLBACK = "Sorry, was hast du gesagt?"
        self.HELP = "Help Intent"

        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]

    def set_generic_phrases_english(self):
        self.ERROR = "Error"
        self.BACKEND_EXCEPTION = "This is an error that shouldn't happen. I am sorry."
        self.SERVER_ERROR = "Due to updates the service is currently not available." \
                            " Try again later."
        self.ACCOUNT_LINKING_REQUIRED = "You must have a {} account to use this skill." \
                                        " Before you can use this skill go to the Alexa app to link your Amazon account" \
                                        " with your {} Account.".format(self.skill_name,
                                                                        self.skill_name)

        self.WRONG_INTENT = "I didn't quite catch that. I can't help you here."

        self.ACKS = ["Okay", "Alright"]
        self.ACCEPTANCE_ACKS = ["Okay", "Sure", "Alright", "Got it", "You got it"]
        self.DONE_ACKS = ["Okay", "Sure", "Alright", "Got it", "Done", "You got it"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Anything else?", "Will that be all?",
                              "Do you need anything else?", "Is there something else you need?"]

        ##############################
        # Required intents
        ##############################
        self.WELCOME = "Welcome"
        self.FALLBACK = "Sorry, what did you say?"
        self.HELP = "Help Intent"
        self.GOODBYES = ["adiós", "aloha", "arrivederci", "ciao", "auf Wiedersehen", "au revoir",
                         "bon voyage", "shalom", "vale"]

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
        random_anyting_else = random.choice(self.GOODBYES)
        self.get_random_done_ack() + ". " + random_anyting_else
