from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from src.skill.i18n.language_model import LanguageModel
from src.skill.services.telethon_service import TelethonService


class MessageIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        user_is_authorized = sess_attrs.get("ACCOUNT").get("AUTHORIZED")
        return is_intent_name("MessageIntent")(handler_input) and user_is_authorized

    def handle(self, handler_input):
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
        speech_text = self.get_telegram(handler_input)
        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(i18n.FALLBACK)
        return handler_input.response_builder.response

    def get_telegram(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = LanguageModel(handler_input.request_envelope.request.locale)

        if not sess_attrs.get("TELEGRAMS"):
            conversations = self.telethon_service.get_conversations(i18n)
            first_names = self.get_first_names(conversations, i18n)
            contacts = [telegram.sender for telegram in conversations]
            spoken_telegrams = self.spoken_telegrams(conversations, i18n)

            sess_attrs["TELEGRAMS"] = spoken_telegrams
            sess_attrs["TELEGRAMS_COUNTER"] = 0
            sess_attrs["CONTACTS"] = contacts

            speech_text = i18n.NEW_TELEGRAMS + first_names
            speech_text = speech_text + spoken_telegrams[sess_attrs["TELEGRAMS_COUNTER"]]
            speech_text = speech_text + i18n.REPLY

            sess_attrs["TELEGRAMS_COUNTER"] += 1
        elif sess_attrs["TELEGRAMS_COUNTER"] < len(sess_attrs["TELEGRAMS"]):
            speech_text = sess_attrs["TELEGRAMS"][sess_attrs["TELEGRAMS_COUNTER"]]
            speech_text = speech_text + i18n.REPLY
            sess_attrs["TELEGRAMS_COUNTER"] += 1
        else:
            speech_text = i18n.NO_MORE_TELEGRAMS
            sess_attrs.pop("TELEGRAMS")
            sess_attrs.pop("TELEGRAMS_COUNTER")
        return speech_text

    def get_first_names(self, conversations, i18n):
        first_names = []

        # Don't loop over last, because we add an 'and' for the voice output
        if len(conversations) > 1:
            for telegram in conversations[:-1]:
                first_names.append(telegram.sender)
            first_names = ", ".join(first_names)
            first_names += i18n.AND + conversations[-1].sender + ". <break time='200ms'/>"
        else:
            first_names = conversations[0].sender + ". <break time='200ms'/>"

        # Constructs a string like: "Tom, Paul, and Julia"
        return first_names

    def spoken_telegrams(self, conversations, i18n):
        texts = []

        for conversation in conversations:
            if conversation.is_group:
                speech_text = i18n.GROUP_INTRO.format(conversation.sender)
            else:
                speech_text = i18n.PERSONAL_CHAT_INTRO.format(conversation.sender)

            telegrams = " ".join(conversation.telegrams)
            speech_text += telegrams

            texts.append(speech_text)

        return texts
