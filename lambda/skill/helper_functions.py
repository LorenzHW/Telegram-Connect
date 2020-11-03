from six import PY3
from html.parser import HTMLParser


def remove_ssml_tags(ssml_speech):
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


class ExploreIntents:
    EXPLORE_SETUP_INTENT = "asked_to_explore_setup_intent"
    EXPLORE_MESSAGE_INTENT = "asked_to_explore_message_intent"


def set_explore_sess_attr(sess_attrs, explore_intent: str):
    sess_attrs["explore_intent"] = explore_intent
