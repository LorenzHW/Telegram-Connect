from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name

from src.skill.i18n.language_model import LanguageModel
from src.skill.intents.message_intent import MessageIntentHandler
from src.skill.services.telethon_service import TelethonService


class YesIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        previous_intent = sess_attrs.get("PREV_INTENT")

        # User answered Yes on question: "Do you want to reply?"
        if previous_intent == "AMAZON.YesIntent" or previous_intent == "AMAZON.NoIntent" and \
                sess_attrs.get("TELEGRAMS"):
            speech_text = "Ok, let's send a Telegram"
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response

        # User answered Yes on question: "Is there anything else I can help you with?"
        if previous_intent == "SendIntent" or previous_intent == "AMAZON.YesIntent" or previous_intent == "AMAZON.NoIntent" \
                and not sess_attrs.get("TELEGRAMS"):
            speech_text = "I can help you to send a Telegram or check for new Telegrams. So, which do you need?"
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response

        if previous_intent == "LaunchIntent":
            speech_text = MessageIntentHandler().get_messages(handler_input)
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response


class NoIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
        sess_attrs = handler_input.attributes_manager.session_attributes
        previous_intent = sess_attrs.get("PREV_INTENT")

        if previous_intent == "SendIntent":
            speech_text = i18n.get_random_ack() + ", " + i18n.get_random_goodbye()
            handler_input.response_builder.speak(speech_text).set_should_end_session(True)

        # User answered No on the question if he wants to reply
        if (previous_intent == "AMAZON.YesIntent" or previous_intent == "AMAZON.NoIntent") and \
                sess_attrs.get("TELEGRAMS"):
            speech_text = MessageIntentHandler().get_messages(handler_input)
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response

        # User answered Yes on question: "Is there anything else I can help you with?
        if previous_intent == "AMAZON.YesIntent" or previous_intent == "AMAZON.NoIntent" \
                and not sess_attrs.get("TELEGRAMS"):
            speech_text = i18n.get_random_ack() + ", " + i18n.get_random_goodbye()
            handler_input.response_builder.speak(speech_text).set_should_end_session(True)
            return handler_input.response_builder.response

        if previous_intent == "LaunchIntent":
            speech_text = i18n.get_random_ack() + ", I can help you to send a Telegram or check for new Telegrams. So, which do you need?"
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)

        return handler_input.response_builder.response
