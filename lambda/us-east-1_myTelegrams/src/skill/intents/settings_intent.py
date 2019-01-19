from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.dialog import ElicitSlotDirective, DelegateDirective
from ask_sdk_model import Intent

from src.skill.i18n.language_model import LanguageModel


class SettingsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        user_is_authorized = sess_attrs.get("ACCOUNT").get("AUTHORIZED")
        return is_intent_name("SettingsIntent")(handler_input) and user_is_authorized

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
        current_intent = handler_input.request_envelope.request.intent

        for slot_name, current_slot in current_intent.slots.items():
            if slot_name == 'enable_non_verbose_mode':
                if current_slot.value is None:
                    speech_text = i18n.SETTINGS_OPENED
                    slot_to_elicit = 'enable_non_verbose_mode'
                    elicit_directive = ElicitSlotDirective(
                        current_intent, slot_to_elicit)
                    handler_input.response_builder.add_directive(
                        elicit_directive)
                else:
                    speech_text = i18n.NON_VERBOSE_CHOICE.format(
                        current_slot.value)
                    speech_text += ' ' + i18n.LEAVING_SETTINGS_MODE
                    speech_text += ' ' + i18n.get_random_anyting_else_without_ack()

        handler_input.response_builder \
            .speak(speech_text).set_should_end_session(False).ask(i18n.FALLBACK)
        return handler_input.response_builder.response
