from src.skill.i18n.generic_language_model import GenericLanguageModel


class LanguageModel(GenericLanguageModel):
    def __init__(self, locale):
        super().__init__(locale)
        self.FIRST_NAME = None
        self.MESSAGE = None
        self.NO_CONTACT = None
        self.ANYTHING_ELSE = None

        if locale == "de-DE":
            self.set_german_language_model()
        else:
            self.set_english_language_model()

    def set_german_language_model(self):
        self.FIRST_NAME = None
        self.MESSAGE = None
        self.NO_CONTACT = None
        self.ANYTHING_ELSE = None

    def set_english_language_model(self):
        self.FIRST_NAME = "{}, what is the first name of your contact?".format(
            self.get_random_ack())
        self.MESSAGE = self.get_random_acceptance_ack() + ", what is the message for {}"
        self.NO_CONTACT = self.get_random_thinking() + ", I can't find any contact with that name. I found {}, {}, and {}. To whom should I send the Telegram?"
        self.ANYTHING_ELSE = self.get_random_done_ack() + ". Is there anything else I can help you with?"
