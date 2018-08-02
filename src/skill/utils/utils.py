from difflib import SequenceMatcher
from html.parser import HTMLParser

from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective
from six import PY3

############## PARSER ##############
from src.skill.i18n.language_model import LanguageModel
from src.skill.services.telethon_service import TelethonService


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


def handle_authorization(handler_input):
    i18n = LanguageModel(handler_input.request_envelope.request.locale)
    telethon_service = TelethonService()
    sess_attrs = handler_input.attributes_manager.session_attributes
    account = sess_attrs.get("ACCOUNT")
    slots = handler_input.request_envelope.request.intent.slots
    reprompt = None

    if not account.get("PHONE_NUMBER"):
        speech_text = i18n.NO_PHONE
        should_end = True
    elif not slots.get("code").value:
        phone_code_hash = telethon_service.send_code_request()
        sess_attrs["PHONE_CODE_HASH"] = phone_code_hash

        updated_intent = Intent("CustomYesIntent", slots)
        elicit_directive = ElicitSlotDirective(updated_intent, "code")
        handler_input.response_builder.add_directive(elicit_directive)

        speech_text = i18n.WHAT_IS_CODE
        reprompt = i18n.WHAT_IS_CODE_REPROMPT
        should_end = False
    else:
        phone_code_hash = sess_attrs.get("PHONE_CODE_HASH")
        ok = telethon_service.sign_user_in(slots.get("code").value, phone_code_hash)

        if ok:
            sess_attrs["ACCOUNT"]["AUTHORIZED"] = True
            speech_text = i18n.AUTHORIZED
            reprompt = i18n.FALLBACK
        else:
            speech_text = i18n.WRONG_CODE
            should_end = True

    handler_input.response_builder.speak(speech_text) \
        .set_should_end_session(should_end)
    if reprompt:
        handler_input.response_builder.ask(reprompt)
    return handler_input


def respond_to_http_error_code(handler_input, http_error_code):
    i18n = LanguageModel(handler_input.request_envelope.request.locale)
    sess_attrs = handler_input.attributes_manager.session_attributes

    if http_error_code == 401:
        # Unauthorized: Happens when user enables alexa skill with valid account
        # then deletes account on my webserver and uses skill again
        speech_text = i18n.ACCOUNT_LINKING_REQUIRED
        sess_attrs["LINK_ACCOUNT_CARD"] = True
    elif 500 <= http_error_code < 600:
        speech_text = i18n.SERVER_ERROR
    else:
        speech_text = i18n.BACKEND_EXCEPTION

    handler_input.response_builder.speak(speech_text).set_should_end_session(True)
    return handler_input.response_builder.response


class BackendException(Exception):
    def __init__(self, message):
        super(BackendException, self).__init__(message)
