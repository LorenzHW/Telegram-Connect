from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from src.skill.i18n.language_model import LanguageModel
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.exceptions import TelethonException, handle_telethon_error_response, AccountException
from src.skill.utils.constants import Constants
from src.skill.utils.utils import check_for_account


class MessageIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("MessageIntent")(handler_input)

    def handle(self, handler_input):
        try:
            check_for_account(handler_input)
        except AccountException as error:
            return handler_input.response_builder \
                .speak(error.args[0]).set_should_end_session(True).response

        i18n = Constants.i18n
        speech_text = self.get_telegram(handler_input)
        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(i18n.FALLBACK)
        return handler_input.response_builder.response

    def get_telegram(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = Constants.i18n

        if not sess_attrs.get("TELEGRAMS"):
            try:
                conversations = self.telethon_service.get_conversations(i18n)
            except TelethonException as error:
                return handle_telethon_error_response(error, handler_input)

            if len(conversations) == 0:
                speech_text = i18n.NO_TELEGRAMS
                return speech_text

            first_names = self.get_first_names(conversations, i18n)
            contacts = [telegram.sender for telegram in conversations]
            entity_ids = [telegram.entity_id for telegram in conversations]
            spoken_telegrams = self.spoken_telegrams(conversations, i18n)

            sess_attrs["TELEGRAMS"] = spoken_telegrams
            sess_attrs["TELEGRAMS_COUNTER"] = 0
            sess_attrs["CONTACTS"] = contacts
            sess_attrs["ENTITY_IDS"] = entity_ids

            speech_text = i18n.NEW_TELEGRAMS + first_names
            speech_text = speech_text + \
                spoken_telegrams[sess_attrs["TELEGRAMS_COUNTER"]]

            if len(conversations) == 1:
                speech_text += i18n.REPLY_SEND_OR_STOP
                sess_attrs.pop("TELEGRAMS")
                sess_attrs.pop("TELEGRAMS_COUNTER")
            else:
                speech_text += i18n.REPLY_OR_NEXT_TELEGRAM
                sess_attrs["TELEGRAMS_COUNTER"] += 1

        elif sess_attrs["TELEGRAMS_COUNTER"] < len(sess_attrs["TELEGRAMS"]) - 1:
            speech_text = sess_attrs["TELEGRAMS"][sess_attrs["TELEGRAMS_COUNTER"]]
            speech_text = speech_text + i18n.REPLY_OR_NEXT_TELEGRAM
            sess_attrs["TELEGRAMS_COUNTER"] += 1
        else:
            speech_text = sess_attrs["TELEGRAMS"][sess_attrs["TELEGRAMS_COUNTER"]]
            speech_text += i18n.REPLY_SEND_OR_STOP
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
            first_names += i18n.AND + \
                conversations[-1].sender + ". " + i18n.BREAK_BETWEEN_NAMES
        else:
            first_names = conversations[0].sender + \
                ". " + i18n.BREAK_BETWEEN_NAMES

        # Constructs a string like: "Tom, Paul, and Julia"
        return first_names

    def spoken_telegrams(self, conversations, i18n):
        texts = []

        for conversation in conversations:
            if conversation.is_group:
                speech_text = i18n.GROUP_INTRO.format(conversation.sender)
            else:
                speech_text = i18n.PERSONAL_CHAT_INTRO.format(
                    conversation.sender)

            telegrams = " ".join(conversation.telegrams)
            speech_text += telegrams

            texts.append(speech_text)

        return texts
