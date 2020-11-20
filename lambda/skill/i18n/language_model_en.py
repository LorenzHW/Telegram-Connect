from datetime import tzinfo
from skill.i18n.language_model_abc import LanguageModelABC


class LanguageModelEN(LanguageModelABC):
    def __init__(self, timezone: tzinfo):
        self.timezone = timezone
        self.SKILL_NAME = 'Telegram Connect'
        self.SKILL_NAME_SPOKEN_EN = "<lang xml:lang='en-US'>Telegram Connect</lang>".format(self.SKILL_NAME)

        self.set_language_model()

    def set_language_model(self):
        ##############################
        # GeneralStuff
        ##############################
        self.ACKS = ["Okay", "Alright", "Okey Dokey"]
        self.ACCEPTANCE_ACKS = ["Okay", "Sure", "Alright", "Got it", "You got it"]
        self.DONE_ACKS = ["Okay", "Alright", "Got it", "Done", "You got it"]
        self.THINKING = ["Umm", "Ahhm", "Hmmm"]
        self.ANYTHING_ELSE = ["Anything else?", "Is there something else I can help you with?",
                              "Do you need anything else?", "Is there something else you need?"]
        self.GOODBYES = ["Bye", "Goodbye", "Bye-Bye", "See you", "Cheerio", "I'm out", "Take care",
                         "Bye for now", "See you later", "Catch you later", "See you soon", "Talk to you later",
                         "See you next time", "Have a good one", "Have a nice day"]
        self.DONT_UNDERSTAND = ["Sorry", "Excuse me", "Pardon"]

        self.GOOD_EVENING = "Good evening!"
        self.GOOD_MORNING = "Good morning!"
        self.GOOD_AFTERNOON = "Good afternoon!"
        self.GOOD_BYE_EVENING = "Have a nice evening!"
        self.GOOD_BYE_MORNING = "Have a nice day!"

        self.FALLBACK = self.get_random_dont_understand() + ", what did you say?"
        self.EXCEPTION = "An unexpected error happened. If you have some time, please let us know what happened on " \
                         "GitHub. Bye for now."

        ##############################
        # LaunchRequestHandler
        ##############################
        self.WELCOME_BACK = 'Welcome back!'
        self.NO_NEW_TELEGRAMS = "You don't have any new telegrams."
        self.NEW_TELEGRAMS = 'You have new telegrams. Do you want to hear them?'
        self.NEW_SETUP = 'Welcome to {}. {} couples Alexa with your Telegram ' \
                         'Messenger. Now, are you ready to start the setup?'.format(self.SKILL_NAME_SPOKEN_EN,
                                                                                    self.SKILL_NAME_SPOKEN_EN)

        ##############################
        # HelpIntent
        ##############################
        self.HELP = "{} connects your Alexa with your Telegram Messenger. To " \
                    "start the setup say: 'Start the setup'. To check whether you have new telegrams say: 'check my " \
                    "telegrams'. To learn more about the skill say: 'learn more about the skill'. So, what do you " \
                    "want to do?".format(self.SKILL_NAME_SPOKEN_EN)
        self.RATE_SKILL = "If you enjoy {}, share your thoughts by writing a review. We value your " \
                          "opinion very very much and continuously try to improve. Thanks!" \
            .format(self.SKILL_NAME_SPOKEN_EN)

        ##############################
        # SetupIntent
        ##############################
        self.NO_PERMISSION = 'You have not granted permission to {} to access your mobile phone number. ' \
                             'In order to connect your Telegram Messenger to Alexa, access is required. Open the Alexa ' \
                             'App and grant the necessary permissions. Bye for now.'.format(self.SKILL_NAME_SPOKEN_EN)

        self.CODE_SENT = 'Go grab your phone and open up Telegram. ' + self.BREAK_2000 + 'You just received a code. What is the code?'
        self.SUCCESS_SETUP = 'You successfully coupled your Telegram Account. To check whether you received new messages, start the skill again. Bye for now.'
        self.PHONE_CODE_INVALID = '{} is the wrong code. Say the code again now.'
        self.PHONE_CODE_INVALID_2 = '{} is still wrong. Bye for now.'
        self.PHONE_CODE_EXPIRED = 'The code already expired. Bye for now.'
        self.PHONE_NUM_UNOCCUPIED = 'This phone number is not known to Telegram. Please create a Telegram account first. Bye for now.'
        self.TWO_STEP_ON = "You have two-step verification turned on in Telegram. Alexa can't be coupled with Telegram while this is on. Please, first go to telegram and disable two-step verificiation. Then come back and try again. After you successfully coupled Alexa with Telegram, you can turn it on again. Bye for now."
        self.ALREADY_AUTHORIZED = 'You already successfully coupled Alexa with Telegram. Bye for now.'
        self.EXCEPTION_RETRIEVING_PHONE_NUM = 'There was a problem retrieving your phone number from your Amazon profile. Please make sure that you have granted access to Telegram Connect to access your phone number and that you have a valid phone number in your Amazon Profile. Bye for now.'

        ##############################
        # MessageIntent
        ##############################
        self.NEW_TELEGRAMS_FROM = 'You received new telegrams from: {}. '
        self.AND = 'and'
        self.NO_MORE_TELEGRAMS = 'There are no more new telegrams. Bye for now.'
        self.NEXT_TELEGRAMS = 'Do you want to hear the telegrams from your next contact?'
        self.PERSONAL_DIALOG_INTRO = '{} wrote: '
        self.GROUP_DIALOG_INTRO = 'In {}'
        self.MEDIA_FILE_RECEIVED = '{} sent a media file.'
        self.NOT_AUTHORIZED = "You didn't couple Alexa with Telegram. Bye for now."

        ##############################
        # YesIntent
        ##############################
        self.SUGGEST_WHAT_TO_DO = "You can say something like: 'Check my telegrams' or: 'learn more about the skill'. So, what do you want to do?"

        ##############################
        # LearnMoreIntent
        ##############################
        self.LEARN_MORE = '{} couples Alexa with Telegram. The code of this skill is open-source and everyone is more ' \
                          'than welcome to contribute. We are searching for people who translate this skill into ' \
                          'different languages such as spanish and italian. If you have any problems or wish for a ' \
                          'specific feature, feel free to reach out on GitHub. Bye for now.' \
            .format(self.SKILL_NAME_SPOKEN_EN)
