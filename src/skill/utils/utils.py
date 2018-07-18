from difflib import SequenceMatcher
from html.parser import HTMLParser

from six import PY3


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

    for index, name in enumerate(first_names):
        percentage = s.similar(name, slot_value)
        if percentage > 0.7 and percentage > prev_percentage:
            prev_percentage = percentage
            contact = first_names[index]
    return contact


class StringComparer():
    def similar(self, a, b):
        # Lets make uppercase here, for better ratios
        a = a.upper()
        b = b.upper()
        return SequenceMatcher(None, a, b).ratio()


def send_telegram(first_name):
    print("SEND_TELEGRAM CONTACT")
    print(first_name)
    pass
