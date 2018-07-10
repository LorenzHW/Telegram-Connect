from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from src.skill.services.telethon_service import TelethonService


class MessageIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("MessageIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Yo dude, wazz up"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    def get_messages(self, handler_input):
        speech_text = "Yo dude, wazz up"
        return speech_text
