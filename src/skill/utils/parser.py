from difflib import SequenceMatcher
from html.parser import HTMLParser

from six import PY3


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


def convert_speech_to_text(ssml_speech):
    # convert ssml speech to text, by removing html tags
    s = SSMLStripper()
    s.feed(ssml_speech)
    return s.get_data()


class StringComparer():
    def similar(self, a, b):
        # Lets make uppercase here, for better ratios
        a = a.upper()
        b = b.upper()
        return SequenceMatcher(None, a, b).ratio()


def get_most_likely_contact(contacts, slot_value):
    prev_percentage = 0
    s = StringComparer()
    contact = None

    for index, c in enumerate(contacts):
        percentage = s.similar(c.first_name, slot_value)
        print(percentage)
        print("PERCENTAGE")
        print("PERCENTAGE")
        print("PERCENTAGE")
        if percentage > 0.7 and percentage > prev_percentage:
            prev_percentage = percentage
            contact = contacts[index]
    return contact
