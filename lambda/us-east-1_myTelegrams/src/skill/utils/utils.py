from difflib import SequenceMatcher
from html.parser import HTMLParser

from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective
from six import PY3

from src.skill.utils.constants import Constants
from src.skill.i18n.non_verbose_language_model import NonVerboseLanguageModel
from src.skill.services.telethon_service import TelethonService
from src.skill.services.daily_telegrams_service import DailyTelegramsService

############## PARSER ##############
def convert_speech_to_text(ssml_speech):
    # convert ssml speech to text, by removing html tags
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


class SSMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.full_str_list = []
        if PY3:
            self.strict = False
            self.convert_charrefs = True

    def handle_data(self, d):
        self.full_str_list.append(d)

    def get_data(self):
        return ''.join(self.full_str_list)


############## CONTACT SEARCH / COMPARER ##############
def get_most_likely_name(first_names, slot_value):
    prev_percentage = 0
    s = StringComparer()
    contact = None
    list_index = None

    for index, name in enumerate(first_names):
        percentage = s.similar(name, slot_value)
        if percentage > 0.7 and percentage > prev_percentage:
            prev_percentage = percentage
            contact = first_names[index]
            list_index = index
    return contact, list_index


class StringComparer():
    def similar(self, a, b):
        # Lets make uppercase here, for better ratios
        a = a.upper()
        b = b.upper()
        return SequenceMatcher(None, a, b).ratio()

def set_language_model(locale, non_verbose_mode):
    Constants.i18n = NonVerboseLanguageModel(locale, non_verbose_mode)    