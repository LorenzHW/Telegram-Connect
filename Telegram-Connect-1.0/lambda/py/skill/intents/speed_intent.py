from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from skill.i18n.language_model import LanguageModel
from skill.services.daily_telegrams_service import DailyTelegramsService
from skill.services.telethon_service import TelethonService
from skill.utils.exceptions import TelethonException, handle_telethon_error_response, SpeedDialException
from skill.utils.constants import Constants
from skill.utils.utils import handle_speed_dial_number_input, send_telegram


class SpeedIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        user_is_authorized = sess_attrs.get("ACCOUNT", {}).get("AUTHORIZED")
        if is_intent_name("SpeedIntent")(handler_input) and user_is_authorized:
            slots = handler_input.request_envelope.request.intent.slots
            if slots.get('message').value and not slots.get('speed_dial_number').value:
                return False
            return True

    def handle(self, handler_input):
        sess_attrs = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        updated_intent = Intent("SpeedIntent", slots)
        i18n = Constants.i18n

        for slot_name in slots:
            slot = slots[slot_name]
            if slot_name == "speed_dial_number" and slots.get("message").value is None:
                if slot.value is None:
                    slot_to_elicit = "speed_dial_number"
                    speech_text = i18n.SPEED_DIAL
                    reprompt = i18n.SPEED_DIAL_REPROMPT
                else:
                    num = int(slot.value)
                    try:
                        speech_text, reprompt, slot_to_elicit = handle_speed_dial_number_input(
                            num, sess_attrs, i18n)
                    except SpeedDialException as error:
                                return handler_input.response_builder \
                                    .speak(error.args[0]).set_should_end_session(True).response

                directive = ElicitSlotDirective(updated_intent, slot_to_elicit)
                handler_input.response_builder.add_directive(directive)

            if slot.name == "message" and slot.value:
                try:
                    m = slot.value
                    speech_text, reprompt = send_telegram(m, sess_attrs, i18n)
                except TelethonException as error:
                    return handle_telethon_error_response(error, handler_input)

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(reprompt)
        return handler_input.response_builder.response
