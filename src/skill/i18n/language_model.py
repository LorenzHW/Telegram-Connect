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

        self.NOT_AUTHORIZED = None
        self.USER_HAS_TELEGRAMS = None

        self.TELEGRAM_SENT = None
        self.MESSAGE_2 = None
        self.HELP_USER = None
        self.BYE_FOR_NOW = None

        self.NO_PHONE = None
        self.WHAT_IS_CODE = None
        self.AUTHORIZED = None
        self.WRONG_CODE = None

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

        ### LaunchIntent ###
        self.NOT_AUTHORIZED = None
        self.USER_HAS_TELEGRAMS = None
        self.WELCOME = None

        ### YesIntent ###
        self.TELEGRAM_SENT = None
        self.MESSAGE_2 = None
        self.HELP_USER = None
        self.BYE_FOR_NOW = None

        self.NO_PHONE = None
        self.WHAT_IS_CODE = None
        self.AUTHORIZED = None
        self.WRONG_CODE = None

    def set_english_language_model(self):
        ### SendIntent ###
        self.FIRST_NAME = "{}, what is the first name of your contact?".format(
            self.get_random_ack())
        self.MESSAGE = self.get_random_acceptance_ack() + ", what is the Telegram for {}?"
        self.NO_CONTACT = self.get_random_thinking() + ", I can't find any contact with that name. I found {}, {}, and {}. To whom should I send the Telegram?"
        self.MAX_NO_CONTACT = "Sorry. I am still having trouble, so you may want to visit the website and try the speed dial feature. " + self.get_random_goodbye()

        ### MessageIntent ###
        self.REPLY = "<break time='200ms'/> Do you want to reply?"
        self.NEW_TELEGRAMS = "You got new Telegrams from: "
        self.NO_MORE_TELEGRAMS = "There are no more Telegrams. Is there anything else I can help you with?"
        self.AND = ", and "
        self.GROUP_INTRO = "In {}: <break time='200ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} wrote: <break time='200ms'/>"

        ### LaunchIntent ###
        self.NOT_AUTHORIZED = "Welcome to {}. {} let's you connect your Telegram Messenger with Alexa. Now, you are currently not authorized." \
            .format(self.skill_name, self.skill_name)
        self.USER_HAS_TELEGRAMS = "Welcome to {}. You got new telegrams. Do you want to hear them?" \
            .format(self.skill_name)
        self.WELCOME = "Welcome to {}. I can help you to send a Telegram or check for new Telegrams. So, which do you need?" \
            .format(self.skill_name)

        ### YesIntent ###
        self.TELEGRAM_SENT = self.get_random_acceptance_ack() + ", a Telegram was sent to {}"
        self.MESSAGE_2 = self.get_random_acceptance_ack() + ", what is the Telegram?"
        self.HELP_USER = "I can help you to send a Telegram or check for new Telegrams. So, which do you need?"
        self.BYE_FOR_NOW = "Bye for now."

        self.NO_PHONE = "You have not added a telephone number. Visit the website mentioned in the skill description and add a telephone number then try again. Bye for now."
        self.WHAT_IS_CODE = "You received a code on your phone. <break time='200ms' /> What is the code?"
        self.AUTHORIZED = self.get_random_acceptance_ack() + ". You are now authorized. <break time='200ms'/> I can help you send a Telegram or check for new Telegrams. So, which do you need?"
        self.WRONG_CODE = "The code is wrong. Try requesting a new code by starting over. Bye for now."
