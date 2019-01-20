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
        self.NO_MORE_TELEGRAMS = None
        self.NO_TELEGRAMS = None
        self.AND = None
        self.GROUP_INTRO = None
        self.GROUP_MESSAGE_INTRO = None
        self.PERSONAL_CHAT_INTRO = None
        self.MEDIA_FILE = None

        self.NOT_AUTHORIZED = None
        self.USER_HAS_TELEGRAMS = None

        self.TELEGRAM_SENT = None
        self.MESSAGE_2 = None
        self.HELP_USER = None
        self.BYE_FOR_NOW = None

        self.NO_PHONE = None
        self.WHAT_IS_CODE = None
        self.WHAT_IS_CODE_REPROMPT = None
        self.AUTHORIZED = None
        self.WRONG_CODE = None

        self.SPEED_DIAL = None
        self.SPEED_DIAL_REPROMPT = None
        self.NO_SPEED_DIAL_CONTACT = None
        self.MULTIPLE_TELEGRAM_CONTACTS_FOR_SPEED_DIAL = None

        self.SETTINGS_OPENED = None
        self.NON_VERBOSE_CHOICE = None
        self.LEAVING_SETTINGS_MODE = None

        self.INVALID_PHONE = None
        self.CODE_EXPIRED = None
        self.CODE_INVALID = None
        self.TWO_STEPS_VERIFICATION_ERROR = None
        self.FLOODWAIT_ERROR = None
        self.CHAT_ADMIN_REQUIRED_ERROR = None
        self.NOT_AUTHORIZED_DETOUR = None

    def set_german_language_model(self):
        pass

    def set_english_language_model(self):
        ### SendIntent ###
        self.FIRST_NAME = "{}, what is the first name of your contact?".format(
            self.get_random_ack())
        self.FIRST_NAME_REPROMPT = self.get_random_dont_understand() + ", what was the first name?"
        self.MESSAGE = "What is the Telegram for {}?"
        self.MESSAGE_REPROMPT = self.get_random_dont_understand() + ", what is the Telegram for {}?"
        self.NO_CONTACT = self.get_random_thinking() + ", I can't find any contact with that name. I found: <break time='100ms'/> 1 <break time='150ms'/> {}, <break time='100ms'/> 2 <break time='150ms'/> {}, and <break time='100ms'/> 3 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.NO_CONTACT_2 = self.get_random_thinking() + ", I can't find any contact with that name. I found <break time='100ms'/> 1 <break time='150ms'/> {}, and <break time='100ms'/> 2 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.NO_CONTACT_REPROMPT = self.get_random_dont_understand() + ", I didn't catch that. I found: <break time='100ms'/> 1 <break time='150ms'/> {}, <break time='100ms'/> 2 <break time='150ms'/> {}, and <break time='100ms'/> 3 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.NO_CONTACT_REPROMPT_2 = self.get_random_dont_understand() + ", I didn't catch that. I found: <break time='100ms'/> 1 <break time='150ms'/> {}, and <break time='100ms'/> 2 <break time='150ms'/> {}. To whom should I send the Telegram?"
        self.MAX_NO_CONTACT = "Sorry. I am still having trouble understanding you. Please say: <break time='100ms'/> 1 <break time='150ms'/> <break time='100ms'/> 2 <break time='150ms'/> or <break time='100ms'/> 3 <break time='150ms'/>. Otherwise you can try out the speed dial feature. Check the skill description for more information. " + self.get_random_goodbye()

        ### MessageIntent ###
        self.REPLY = "<break time='250ms'/> Do you want to reply or listen to the next Telegram?"
        self.NEW_TELEGRAMS = "You got new Telegrams from: "
        self.NO_MORE_TELEGRAMS = "There are no more Telegrams. Is there anything else I can help you with?"
        self.NO_TELEGRAMS = "You got no new telegrams. " + self.get_random_anyting_else_without_ack()
        self.AND = ", and "
        self.GROUP_INTRO = "In {}: <break time='200ms'/>"
        self.GROUP_MESSAGE_INTRO = "{} wrote: <break time='100ms'/>"
        self.PERSONAL_CHAT_INTRO = "{} wrote: <break time='200ms'/>"
        self.MEDIA_FILE = "Media file"

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

        ### YesIntent ###
        self.HELP_USER = "I can help you to send a Telegram or check for new Telegrams. So, which do you need?"

        ### AuthorizationIntent ###
        self.NO_PHONE = "You have not added a telephone number. Visit the website mentioned in the skill description and add a telephone number then try again. Bye for now."
        self.WHAT_IS_CODE = "You received a code on your phone. <break time='200ms' /> What is the code?"
        self.WHAT_IS_CODE_REPROMPT = "Check your phone. What is the code?"
        self.WRONG_CODE = "The code is wrong. Try requesting a new code by starting over. Bye for now."
        self.AUTHORIZED = self.get_random_acceptance_ack() + ". You are now authorized. <break time='200ms'/> I can help you send a Telegram or check for new Telegrams. So, which do you need?"

        ## SpeedDialIntent ##
        self.SPEED_DIAL = "What is the number of your speed dial contact?"
        self.SPEED_DIAL_REPROMPT = self.get_random_dont_understand() + ", what number?"
        self.NO_SPEED_DIAL_CONTACT = self.get_random_thinking() + ", I can't find any speed dial contact with that number. Is there anything else I can help you with?"
        self.MULTIPLE_TELEGRAM_CONTACTS_FOR_SPEED_DIAL = self.get_random_thinking() + ", I found multiple contacts with that first name. Please check that the first name of your Telegram contact matches exactly the first name of your speed dial contact. Bye for now."

        ## SettingsIntent ##
        self.SETTINGS_OPENED = 'You are now in the Settings mode. Do you want to enable or disable non-verbose mode?'
        self.NON_VERBOSE_CHOICE = 'You {} non-verbose mode.'
        self.ENABLE = 'enable'
        self.DISABLE = 'disable'
        self.LEAVING_SETTINGS_MODE = 'You are now leaving settings mode.'

        ## Errors ##
        self.INVALID_PHONE = "There is no Telegram account associated with that phone number. Create a Telegram Account first, before you can use that skill. Bye for now."
        self.CODE_EXPIRED = "The code already expired. Try it again. Bye for now."
        self.CODE_INVALID = "The code is invalid. Bye for now."
        self.TWO_STEPS_VERIFICATION_ERROR = "Two step verification is not supported. Please deactivate two step verficication in Telegram to use this skill. Bye for now."
        self.FLOODWAIT_ERROR = "The skill is unavailable due to server maintenance. You can use this skill in {} hours and {} minutes. Bye for now."
        self.CHAT_ADMIN_REQUIRED_ERROR = "You don't have the privilege to send a Telegram."
        self.NOT_AUTHORIZED_DETOUR = "You are currently not authorized. Please authorize first if you want to use all features of this skill. To start the authorization process say: 'Alexa, start {}'. Bye for now".format(
            self.skill_name)
        self.BYE_FOR_NOW = "Bye for now."
