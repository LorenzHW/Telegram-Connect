from difflib import SequenceMatcher
from html.parser import HTMLParser

from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective
from six import PY3

from src.skill.utils.constants import Constants
from src.skill.i18n.non_verbose_language_model import NonVerboseLanguageModel
from src.skill.services.telethon_service import TelethonService
from src.skill.services.daily_telegrams_service import DailyTelegramsService
from src.skill.services.daily_telegrams_service import DailyTelegramsService
from src.skill.utils.exceptions import SpeedDialException

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


def handle_speed_dial_number_input(number, sess_attrs, i18n):
    dt_service = DailyTelegramsService()
    telethon_service = TelethonService()

    slot_to_elicit = "message"
    first_name = dt_service.get_firstname_for_speed_dial_number(
        number)
    if first_name:
        contacts = telethon_service.get_potential_contacts(first_name)

        if len(contacts) > 1:
            error_message = i18n.MULTIPLE_TELEGRAM_CONTACTS_FOR_SPEED_DIAL
            raise SpeedDialException(error_message)

        c = contacts[0]
        speech_text = i18n.MESSAGE.format(c.first_name)
        reprompt = i18n.MESSAGE.format(c.first_name)

        sess_attrs["FIRST_NAMES"] = [c.first_name]
        sess_attrs["TELETHON_ENTITY_ID"] = c.entity_id

        return (speech_text, reprompt, slot_to_elicit)
    else:
        error_message = i18n.NO_SPEED_DIAL_CONTACT
        raise SpeedDialException(error_message)



def send_telegram(message, sess_attrs, i18n):
        entity_id = sess_attrs.get("TELETHON_ENTITY_ID")
        TelethonService().send_telegram(entity_id, message)
        speech_text = i18n.get_random_anyting_else()
        reprompt = i18n.FALLBACK
        sess_attrs.clear()
        return speech_text, reprompt


def parse_spoken_numbers_to_integers(spoken_number):
    mapping = {
        'eins': "1",
        "zwei": "2",
        "drei": "3",
        "vier": "4",
        "fünf": "5",
        "sechs": "6",
        "sieben": "7",
        "acht": "8",
        "neun": "9",
        "zehn": "10",
        "elf": "11",
        "zwölf": "12",
        "dreizehn": "13",
        "vierzehn": "14"
    }
    return mapping[spoken_number]