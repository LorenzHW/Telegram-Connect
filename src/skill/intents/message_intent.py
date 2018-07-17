from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from src.skill.services.telethon_service import TelethonService


class MessageIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("MessageIntent")(handler_input)

    def handle(self, handler_input):
        telegrams = self.telethon_service.get_conversations()
        speech_text = "You got new Telegrams from: " + self.get_first_names(telegrams)
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

    def get_messages(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes

        if not sess_attrs.get("TELEGRAMS"):
            conversations = self.telethon_service.get_conversations()
            first_names = self.get_first_names(conversations)
            speech_texts = self.construct_speech_texts(conversations)
            sess_attrs["TELEGRAMS"] = speech_texts
            sess_attrs["TELEGRAMS_COUNTER"] = 0
            speech_text = "You got new Telegrams from: " + first_names
            speech_text = speech_text + sess_attrs["TELEGRAMS"][sess_attrs["TELEGRAMS_COUNTER"]]
            speech_text = speech_text + "<break time='200ms'/> Do you want to reply?"
            sess_attrs["TELEGRAMS_COUNTER"] += 1
        elif sess_attrs["TELEGRAMS_COUNTER"] < len(sess_attrs["TELEGRAMS"]):
            speech_text = sess_attrs["TELEGRAMS"][sess_attrs["TELEGRAMS_COUNTER"]]
            speech_text = speech_text + "<break time='200ms'/> Do you want to reply?"
            sess_attrs["TELEGRAMS_COUNTER"] += 1
        else:
            speech_text = "There are no more Telegrams. Is there anything else I can help you with?"
            sess_attrs.pop("TELEGRAMS")
            sess_attrs.pop("TELEGRAMS_COUNTER")
        return speech_text

    def get_first_names(self, telegrams):
        first_names = []

        for telegram in telegrams[:-1]:
            first_names.append(telegram.sender)

        first_names = ", ".join(first_names) + ", and " + telegrams[
            -1].sender + ". <break time='200ms'/>"

        return first_names

    def construct_speech_texts(self, conversations):
        texts = []

        for conversation in conversations:
            if conversation.is_group:
                speech_text = "In {}: <break time='200ms'/>".format(conversation.sender)
            else:
                speech_text = "{} wrote: <break time='200ms'/>".format(conversation.sender)

            telegrams = " ".join(conversation.telegrams)
            speech_text += telegrams

            texts.append(speech_text)

        return texts
