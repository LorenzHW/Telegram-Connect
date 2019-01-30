from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.dialog import ElicitSlotDirective, DelegateDirective
from ask_sdk_model import Intent

from src.skill.intents.message_intent import MessageIntentHandler
from src.skill.services.telethon_service import TelethonService
from src.skill.i18n.language_model import LanguageModel
from src.skill.utils.constants import Constants


class ReplyIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        user_is_authorized = sess_attrs.get("ACCOUNT", {}).get("AUTHORIZED")
        return is_intent_name("ReplyIntent")(handler_input) and user_is_authorized

    def handle(self, handler_input):
        self.telethon_service = TelethonService()
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = Constants.i18n
        slots = handler_input.request_envelope.request.intent.slots

        if slots.get("message").value:
            if sess_attrs.get("TELEGRAMS_COUNTER") is None:
                # User is replying on last unread dialog
                index = len(sess_attrs.get("CONTACTS")) - 1
            else:
                # User is replying to some other dialog
                index = sess_attrs.get("TELEGRAMS_COUNTER") - 1

            contact = sess_attrs.get("CONTACTS")[index]
            entity_id = sess_attrs.get("ENTITY_IDS")[index]
            self.telethon_service \
                .send_telegram(entity_id, slots.get("message").value)

            next_telegram = MessageIntentHandler().get_telegram(handler_input)
            speech_text = i18n.TELEGRAM_SENT.format(contact) + next_telegram
            reprompt = i18n.FALLBACK
        else:
            speech_text = i18n.get_random_acceptance_ack() + ", " + i18n.MESSAGE_2
            reprompt = i18n.get_random_dont_understand() + ", " + i18n.MESSAGE_2
            updated_intent = Intent("ReplyIntent", slots)
            elicit_directive = ElicitSlotDirective(updated_intent, "message")
            handler_input.response_builder.add_directive(elicit_directive)

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
