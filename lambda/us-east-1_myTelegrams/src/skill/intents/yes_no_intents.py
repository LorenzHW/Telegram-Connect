from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.i18n.language_model import LanguageModel
from src.skill.intents.message_intent import MessageIntentHandler
from src.skill.services.daily_telegrams_service import DailyTelegramsService
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.constants import Constants


class YesIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()
        self.daily_telegrams_service = DailyTelegramsService()

    def can_handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        # If Alexa is user listening for message slot on SendIntent it happens that she hears
        # 'yes' and therefore executes this intent handler. We don't want that.
        return is_intent_name("AMAZON.YesIntent")(handler_input) and not sess_attrs.get(
            "TELETHON_ENTITY_ID")

    def handle(self, handler_input):
        i18n = Constants.i18n
        sess_attrs = handler_input.attributes_manager.session_attributes
        previous_intent = sess_attrs.get("PREV_INTENT")
        user_is_authorized = sess_attrs.get("ACCOUNT").get("AUTHORIZED")

        # User answered Yes on question: "Welcome, do you want to hear your new Telegrams?"
        if previous_intent == "LaunchIntent" and user_is_authorized:
            speech_text = MessageIntentHandler().get_telegram(handler_input)
            handler_input.response_builder.speak(speech_text) \
                .set_should_end_session(False).ask(i18n.FALLBACK)
            return handler_input.response_builder.response

        # User answered Yes on question: "Is there anything else I can help you with?"
        if (previous_intent == "SendIntent"
            or previous_intent == "MessageIntent"
            or previous_intent == "SpeedIntent"
            or previous_intent == "ReplyIntent"
            or previous_intent == "SettingsIntent"
            or previous_intent == "AuthorizationIntent"
            or previous_intent == "AMAZON.YesIntent"
            or previous_intent == "AMAZON.NoIntent") \
                and not sess_attrs.get("TELEGRAMS") and not sess_attrs.get("FIRST_NAMES"):
            speech_text = i18n.HELP_USER
            reprompt = i18n.FALLBACK
            handler_input.response_builder.speak(speech_text) \
                .set_should_end_session(False).ask(reprompt)
            return handler_input.response_builder.response


class NoIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        # If Alexa is user listening for message slot on SendIntent it happens that she hears
        # 'yes' and therefore executes this intent handler. We don't want that.
        return is_intent_name("AMAZON.NoIntent")(handler_input) and not sess_attrs.get(
            "TELETHON_ENTITY_ID")

    def handle(self, handler_input):
        i18n = Constants.i18n
        sess_attrs = handler_input.attributes_manager.session_attributes
        previous_intent = sess_attrs.get("PREV_INTENT")
        user_is_authorized = sess_attrs.get("ACCOUNT").get("AUTHORIZED")

        # User answered No on question: "Welcome, do you want to hear your new Telegrams?"
        if previous_intent == "LaunchIntent" and user_is_authorized:
            speech_text = i18n.get_random_ack() + ", " + i18n.HELP_USER
            handler_input.response_builder.speak(speech_text) \
                .set_should_end_session(False).ask(i18n.FALLBACK)
            return handler_input.response_builder.response

        # User answered No on question: "Is there anything else I can help you with?
        if (previous_intent == "SendIntent"
                or previous_intent == "MessageIntent"
                or previous_intent == "SpeedIntent"
                or previous_intent == "ReplyIntent"
                or previous_intent == "SettingsIntent"
                or previous_intent == "AuthorizationIntent"
                or previous_intent == "AMAZON.YesIntent"
                or previous_intent == "AMAZON.NoIntent") \
                and not sess_attrs.get("TELEGRAMS") and not sess_attrs.get('FIRST_NAMES'):
            speech_text = i18n.get_random_ack() + ", " + i18n.get_random_goodbye()
            handler_input.response_builder.speak(
                speech_text).set_should_end_session(True)
            return handler_input.response_builder.response

        if (previous_intent == "SendIntent"
                or previous_intent == "SpeedIntent"
                or previous_intent == "MessageIntent"
                or previous_intent == "ReplyIntent"
                or previous_intent == "AuthorizationIntent"):
            speech_text = i18n.get_random_ack() + ", " + i18n.get_random_goodbye()
            handler_input.response_builder.speak(
                speech_text).set_should_end_session(True)
            return handler_input.response_builder.response
