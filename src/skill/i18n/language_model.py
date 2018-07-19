from src.skill.i18n.generic_language_model import GenericLanguageModel


class LanguageModel(GenericLanguageModel):
    def __init__(self, locale):
        super().__init__(locale)
        self.FIRST_NAME = None
        self.MESSAGE = None
        self.NO_CONTACT = None
        self.MAX_NO_CONTACT = None

        self.REPLY = None
        self.NEW_TELEGRAMS = None
        self.NO_MORE_TELEGRAMS = None
        self.AND = None
        self.GROUP_INTRO = None
        self.PERSONAL_CHAT_INTRO = None

        if locale == "de-DE":
            self.set_german_language_model()
        else:
            self.set_english_language_model()

    def set_german_language_model(self):
        ### SendIntent ###
        self.FIRST_NAME = None
        self.MESSAGE = None
        self.NO_CONTACT = None
        self.MAX_NO_CONTACT = None

        ### MessageIntent ###
        self.REPLY = None
        self.NEW_TELEGRAMS = None
        self.NO_MORE_TELEGRAMS = None
        self.AND = None
        self.GROUP_INTRO = None
        self.PERSONAL_CHAT_INTRO = None

    def set_english_language_model(self):
        ### SendIntent ###
        self.FIRST_NAME = "{}, what is the first name of your contact?".format(
            self.get_random_ack())
        self.MESSAGE = self.get_random_acceptance_ack() + ", what is the message for {}"
        self.NO_CONTACT = self.get_random_thinking() + ", I can't find any contact with that name. I found {}, {}, and {}. To whom should I send the Telegram?"
        self.MAX_NO_CONTACT = "Sorry. I am still having trouble, so you may want to visit the website and try the speed dial feature. " + self.get_random_goodbye()

        ### MessageIntent ###
        self.REPLY = "<break time='200ms'/> Do you want to reply?"
        self.NEW_TELEGRAMS = "You got new Telegrams from: "
        self.NO_MORE_TELEGRAMS = "There are no more Telegrams. Is there anything else I can help you with?"
        self.AND = ", and "
        self.GROUP_INTRO = "In {}: <break time='200ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} wrote: <break time='200ms'/>"
