import abc
import random
from datetime import datetime, tzinfo
from typing import List


class LanguageModelABC(abc.ABC):
    timezone: tzinfo
    SKILL_NAME: str
    SKILL_NAME_SPOKEN_EN: str

    ##############################
    # GeneralStuff
    ##############################
    BREAK_50 = "<break time='50ms'/>"
    BREAK_75 = "<break time='75ms'/>"
    BREAK_100 = "<break time='100ms'/>"
    BREAK_150 = "<break time='150ms'/>"
    BREAK_200 = "<break time='200ms'/>"
    BREAK_350 = "<break time='350ms'/>"
    BREAK_2000 = "<break time='2000ms'/>"

    ACKS: List
    ACCEPTANCE_ACKS: List
    DONE_ACKS: List
    THINKING: List
    ANYTHING_ELSE: List
    GOODBYES: List
    DONT_UNDERSTAND: List

    GOOD_EVENING: str
    GOOD_MORNING: str
    GOOD_AFTERNOON: str
    GOOD_BYE_EVENING: str
    GOOD_BYE_MORNING: str

    FALLBACK: str
    EXCEPTION: str

    ##############################
    # LaunchRequestHandler
    ##############################
    WELCOME_BACK: str
    NO_NEW_TELEGRAMS: str
    NEW_TELEGRAMS: str
    NEW_SETUP: str

    ##############################
    # HelpIntent
    ##############################
    HELP: str
    RATE_SKILL: str

    ##############################
    # SetupIntent
    ##############################
    NO_PERMISSION: str
    NO_PHONE_NUMBER: str
    CODE_SENT: str
    SUCCESS_SETUP: str
    PHONE_CODE_INVALID: str
    PHONE_CODE_INVALID_2: str
    PHONE_CODE_EXPIRED: str
    PHONE_NUM_UNOCCUPIED: str
    TWO_STEP_ON: str
    ALREADY_AUTHORIZED: str
    EXCEPTION_RETRIEVING_PHONE_NUM: str

    ##############################
    # MessageIntent
    ##############################
    NEW_TELEGRAMS_FROM: str
    AND: str
    NO_MORE_TELEGRAMS: str
    NEXT_TELEGRAMS: str
    PERSONAL_DIALOG_INTRO: str
    GROUP_DIALOG_INTRO: str
    MEDIA_FILE_RECEIVED: str
    NOT_AUTHORIZED: str

    ##############################
    # YesIntent
    ##############################
    SUGGEST_WHAT_TO_DO: str

    ##############################
    # LearnMoreIntent
    ##############################
    LEARN_MORE: str

    @abc.abstractmethod
    def set_language_model(self):
        """ Set the language model for the specific language"""
        return

    def get_daytime_greeting(self):
        now = datetime.now(self.timezone)
        if 6 <= now.hour < 12:
            speech_text = self.GOOD_MORNING
        elif now.hour < 18:
            speech_text = self.GOOD_AFTERNOON
        else:
            speech_text = self.GOOD_EVENING
        return speech_text

    def get_random_ack(self):
        return random.choice(self.ACKS)

    def get_random_acceptance_ack(self):
        return random.choice(self.ACCEPTANCE_ACKS)

    def get_random_done_ack(self):
        return random.choice(self.DONE_ACKS)

    def get_random_goodbye(self):
        goodbyes = self.GOODBYES
        now = datetime.now(self.timezone)
        if now.hour < 18:
            goodbyes.append(self.GOOD_BYE_MORNING)
        else:
            goodbyes.append(self.GOOD_EVENING)
        return random.choice(goodbyes)

    def get_random_thinking(self):
        return random.choice(self.THINKING)

    def get_random_anyting_else_with_ack(self):
        random_anyting_else = random.choice(self.ANYTHING_ELSE)
        return self.get_random_done_ack() + ". " + random_anyting_else

    def get_random_anyting_else(self):
        return random.choice(self.ANYTHING_ELSE)

    def get_random_dont_understand(self):
        return random.choice(self.DONT_UNDERSTAND)
