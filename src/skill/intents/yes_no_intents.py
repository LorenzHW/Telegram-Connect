from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.i18n.language_model import LanguageModel
from src.skill.intents.message_intent import MessageIntentHandler
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.utils import send_telegram


class YesIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("CustomYesIntent")(handler_input)

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        previous_intent = sess_attrs.get("PREV_INTENT")

        # User answered Yes on question: "Do you want to reply?"
        if previous_intent == "CustomYesIntent" or previous_intent == "AMAZON.NoIntent" and \
                sess_attrs.get("TELEGRAMS"):
            slots = handler_input.request_envelope.request.intent.slots

            if slots.get("message").value:

                contact = sess_attrs.get("CONTACTS")[sess_attrs.get("TELEGRAMS_COUNTER") - 1]
                send_telegram(contact)
                next_telegram = MessageIntentHandler().get_telegram(handler_input)
                speech_text = "Telegram was sent to {}. ".format(contact) + next_telegram
            else:
                updated_intent = Intent("CustomYesIntent", slots)
                speech_text = "Ok, what is the message?"
                elicit_directive = ElicitSlotDirective(updated_intent, "message")
                handler_input.response_builder.add_directive(elicit_directive)

            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response

        # User answered Yes on question: "Is there anything else I can help you with?"
        if previous_intent == "SendIntent" or previous_intent == "CustomYesIntent" or previous_intent == "AMAZON.NoIntent" \
                and not sess_attrs.get("TELEGRAMS"):
            speech_text = "I can help you to send a Telegram or check for new Telegrams. So, which do you need?"
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response

        # User answered Yes on question: "Welcome, do you want to hear your new Telegrams?"
        if previous_intent == "LaunchIntent":
            speech_text = MessageIntentHandler().get_telegram(handler_input)
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
        if (previous_intent == "CustomYesIntent" or previous_intent == "AMAZON.NoIntent") and \
                sess_attrs.get("TELEGRAMS"):
            speech_text = MessageIntentHandler().get_telegram(handler_input)
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
            return handler_input.response_builder.response

        # User answered Yes on question: "Is there anything else I can help you with?
        if previous_intent == "CustomYesIntent" or previous_intent == "AMAZON.NoIntent" \
                and not sess_attrs.get("TELEGRAMS"):
            speech_text = i18n.get_random_ack() + ", " + i18n.get_random_goodbye()
            handler_input.response_builder.speak(speech_text).set_should_end_session(True)
            return handler_input.response_builder.response

        if previous_intent == "LaunchIntent":
            speech_text = i18n.get_random_ack() + ", I can help you to send a Telegram or check for new Telegrams. So, which do you need?"
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)

        return handler_input.response_builder.response
