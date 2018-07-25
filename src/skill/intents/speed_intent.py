from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import Intent
from ask_sdk_model.dialog import ElicitSlotDirective

from src.skill.i18n.language_model import LanguageModel
from src.skill.services.daily_telegrams_service import DailyTelegramsService
from src.skill.services.telethon_service import TelethonService
from src.skill.utils.utils import send_telegram


class SpeedIntentHandler(AbstractRequestHandler):
    def __init__(self):
        self.telethon_service = TelethonService()

    def can_handle(self, handler_input):
        return is_intent_name("SpeedIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        updated_intent = Intent("SpeedIntent", slots)
        sess_attrs = handler_input.attributes_manager.session_attributes
        i18n = LanguageModel(handler_input.request_envelope.request.locale)
        daily_telegrams_service = DailyTelegramsService()

        for slot_name in slots:
            slot = slots[slot_name]
            if slot_name == "speed_dial_number" and slots.get("message").value is None:
                if slot.value is None:
                    slot_to_elicit = "speed_dial_number"
                    speech_text = i18n.SPEED_DIAL
                    reprompt = i18n.SPEED_DIAL_REPROMPT
                else:
                    slot_to_elicit = "message"
                    contact = daily_telegrams_service.get_contact_for_speed_dial_number(slot.value)
                    if contact:
                        speech_text = i18n.get_random_acceptance_ack() + ", " \
                                      + i18n.MESSAGE.format(contact.first_name)
                        reprompt = i18n.get_random_dont_understand() + ", " \
                                   + i18n.MESSAGE.format(contact.first_name)
                    else:
                        speech_text = i18n.NO_SPEED_DIAL_CONTACT
                        reprompt = i18n.FALLBACK
                        handler_input.response_builder.speak(speech_text) \
                            .set_should_end_session(False).ask(reprompt)

                        return handler_input.response_builder.response
                elicit_directive = ElicitSlotDirective(updated_intent, slot_to_elicit)
                handler_input.response_builder.add_directive(elicit_directive)

            if slot.name == "message" and slot.value:
                send_telegram("NAME OF SEND TELEGRAM")
                speech_text = i18n.get_random_anyting_else()
                reprompt = i18n.FALLBACK
                sess_attrs.clear()

        handler_input.response_builder.speak(speech_text) \
            .set_should_end_session(False).ask(reprompt)

        return handler_input.response_builder.response
